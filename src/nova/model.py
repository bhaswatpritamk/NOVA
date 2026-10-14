"""Nova-Fit Decoder-Only Transformer Architecture.

Implements an original decoder-only Transformer language model trained from scratch,
featuring:
- Token embeddings
- Rotary Position Embeddings (RoPE)
- Causal multi-head self-attention
- Root Mean Square Layer Normalization (RMSNorm)
- SwiGLU feed-forward networks
- Residual pre-norm connections
- Language model output projection
- Next-token prediction with cross-entropy loss
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, Optional, Tuple, Union

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class NovaConfig:
    """Hyperparameter configuration for Nova-Fit Transformer models."""

    vocab_size: int = 2274
    max_seq_len: int = 32
    d_model: int = 64
    n_layers: int = 2
    n_heads: int = 4
    d_ff: Optional[int] = None
    dropout: float = 0.0
    rope_theta: float = 10000.0
    norm_eps: float = 1e-5
    tie_word_embeddings: bool = False
    pad_token_id: int = 0
    initializer_range: float = 0.02

    def __post_init__(self) -> None:
        """Validate architectural parameters and calculate derived dimensions."""
        if not isinstance(self.vocab_size, int) or self.vocab_size <= 0:
            raise ValueError(f"vocab_size must be a positive integer, got {self.vocab_size}")

        if not isinstance(self.max_seq_len, int) or self.max_seq_len <= 0:
            raise ValueError(f"max_seq_len must be a positive integer, got {self.max_seq_len}")

        if not isinstance(self.d_model, int) or self.d_model <= 0:
            raise ValueError(f"d_model must be a positive integer, got {self.d_model}")

        if not isinstance(self.n_layers, int) or self.n_layers <= 0:
            raise ValueError(f"n_layers must be a positive integer, got {self.n_layers}")

        if not isinstance(self.n_heads, int) or self.n_heads <= 0:
            raise ValueError(f"n_heads must be a positive integer, got {self.n_heads}")

        if self.d_model % self.n_heads != 0:
            raise ValueError(
                f"d_model ({self.d_model}) must be divisible by n_heads ({self.n_heads})"
            )

        self.head_dim = self.d_model // self.n_heads
        if self.head_dim % 2 != 0:
            raise ValueError(
                f"head_dim ({self.head_dim} = d_model / n_heads) must be an even integer for RoPE"
            )

        # Default SwiGLU hidden dimension: ~ (8/3) * d_model, rounded to multiple of 16
        if self.d_ff is None:
            raw_d_ff = int(2 * (4 * self.d_model) / 3)
            self.d_ff = ((raw_d_ff + 15) // 16) * 16

        if not isinstance(self.d_ff, int) or self.d_ff <= 0:
            raise ValueError(f"d_ff must be a positive integer, got {self.d_ff}")

        if not (0.0 <= self.dropout < 1.0):
            raise ValueError(f"dropout must be in [0.0, 1.0), got {self.dropout}")

        if self.norm_eps <= 0:
            raise ValueError(f"norm_eps must be positive, got {self.norm_eps}")

        if not (0 <= self.pad_token_id < self.vocab_size):
            raise ValueError(
                f"pad_token_id ({self.pad_token_id}) must be in range [0, vocab_size={self.vocab_size})"
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> NovaConfig:
        """Create configuration from dictionary, ignoring extraneous metadata keys."""
        valid_fields = cls.__dataclass_fields__.keys()
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)

    @classmethod
    def from_json_file(cls, json_path: Union[str, Path]) -> NovaConfig:
        """Load configuration from JSON file."""
        path = Path(json_path)
        if not path.is_file():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def to_json_file(self, json_path: Union[str, Path]) -> None:
        """Save configuration to JSON file."""
        path = Path(json_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)


@dataclass
class CausalLMOutput:
    """Output container for Nova-Fit decoder-only Transformer."""

    logits: torch.Tensor
    loss: Optional[torch.Tensor] = None

    def __iter__(self) -> Iterator[Any]:
        """Allow tuple unpacking: logits, loss = model(input_ids, targets)."""
        yield self.logits
        yield self.loss


class RMSNorm(nn.Module):
    """Root Mean Square Layer Normalization (RMSNorm).

    Normalizes inputs by the root-mean-square of feature values along the last dimension,
    scaled by a learnable weight vector without additive bias.
    """

    def __init__(self, dim: int, eps: float = 1e-5) -> None:
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Compute root-mean-square across hidden dimension
        variance = x.pow(2).mean(-1, keepdim=True)
        return x * torch.rsqrt(variance + self.eps) * self.weight


class RotaryEmbedding(nn.Module):
    """Rotary Position Embedding (RoPE).

    Encodes positional information by applying a rotation matrix to query and key
    representations in the complex plane across pairs of head dimensions.
    """

    def __init__(self, dim: int, max_seq_len: int = 2048, base: float = 10000.0) -> None:
        super().__init__()
        if dim % 2 != 0:
            raise ValueError(f"Rotary embedding dimension must be even, got {dim}")

        self.dim = dim
        self.max_seq_len = max_seq_len
        self.base = base

        # inv_freq: theta_i = base^(-2(i-1)/dim) for i in [1, dim/2]
        inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer("inv_freq", inv_freq, persistent=False)
        self._build_cache(max_seq_len)

    def _build_cache(self, seq_len: int) -> None:
        """Precompute and cache cosine and sine rotary embeddings."""
        t = torch.arange(seq_len, dtype=torch.float32)
        freqs = torch.outer(t, self.inv_freq)
        # Duplicate frequencies to match head_dim
        emb = torch.cat((freqs, freqs), dim=-1)
        self.register_buffer("cos_cached", emb.cos()[None, None, :, :], persistent=False)
        self.register_buffer("sin_cached", emb.sin()[None, None, :, :], persistent=False)

    def forward(
        self, seq_len: int, device: torch.device
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Retrieve precomputed cos and sin slices for sequence length."""
        if seq_len > self.max_seq_len:
            raise ValueError(
                f"Requested sequence length {seq_len} exceeds configured max_seq_len {self.max_seq_len}"
            )

        return (
            self.cos_cached[:, :, :seq_len, :].to(device),
            self.sin_cached[:, :, :seq_len, :].to(device),
        )


def rotate_half(x: torch.Tensor) -> torch.Tensor:
    """Rotate half of the hidden dimensions for RoPE application."""
    half_dim = x.shape[-1] // 2
    x1 = x[..., :half_dim]
    x2 = x[..., half_dim:]
    return torch.cat((-x2, x1), dim=-1)


def apply_rotary_pos_emb(
    q: torch.Tensor,
    k: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Apply rotary position embeddings to query and key tensors."""
    q_rot = (q * cos) + (rotate_half(q) * sin)
    k_rot = (k * cos) + (rotate_half(k) * sin)
    return q_rot, k_rot


class CausalSelfAttention(nn.Module):
    """Causal Multi-Head Self-Attention with RoPE and Scaled Dot-Product Attention."""

    def __init__(self, config: NovaConfig) -> None:
        super().__init__()
        self.d_model = config.d_model
        self.n_heads = config.n_heads
        self.head_dim = config.head_dim
        self.max_seq_len = config.max_seq_len

        # Linear projections for Queries, Keys, Values (bias=False per modern architecture)
        self.q_proj = nn.Linear(config.d_model, config.d_model, bias=False)
        self.k_proj = nn.Linear(config.d_model, config.d_model, bias=False)
        self.v_proj = nn.Linear(config.d_model, config.d_model, bias=False)
        self.out_proj = nn.Linear(config.d_model, config.d_model, bias=False)

        self.attn_dropout = nn.Dropout(config.dropout)
        self.resid_dropout = nn.Dropout(config.dropout)

        # Lower-triangular causal attention mask
        causal_mask = torch.tril(torch.ones(config.max_seq_len, config.max_seq_len, dtype=torch.bool))
        self.register_buffer("causal_mask", causal_mask, persistent=False)

    def forward(
        self,
        x: torch.Tensor,
        cos: torch.Tensor,
        sin: torch.Tensor,
    ) -> torch.Tensor:
        """Forward pass for causal self-attention.

        Args:
            x: Input tensor of shape [batch_size, seq_len, d_model].
            cos: RoPE cosine tensor of shape [1, 1, seq_len, head_dim].
            sin: RoPE sine tensor of shape [1, 1, seq_len, head_dim].

        Returns:
            Output tensor of shape [batch_size, seq_len, d_model].
        """
        B, T, C = x.shape

        # Project Q, K, V and reshape to [B, n_heads, T, head_dim]
        q = self.q_proj(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)

        # Apply Rotary Position Embeddings
        q, k = apply_rotary_pos_emb(q, k, cos, sin)

        # Scaled dot-product attention
        scores = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(self.head_dim))

        # Enforce strict causal masking
        mask = self.causal_mask[:T, :T]
        scores = scores.masked_fill(~mask, float("-inf"))

        # Attention probabilities
        probs = F.softmax(scores, dim=-1)
        probs = self.attn_dropout(probs)

        # Compute context and project back to d_model
        context = probs @ v  # [B, n_heads, T, head_dim]
        context = context.transpose(1, 2).contiguous().view(B, T, C)

        return self.resid_dropout(self.out_proj(context))


class SwiGLU(nn.Module):
    """SwiGLU Feed-Forward Network.

    Computes: FFN(x) = (SiLU(x * W_gate) * (x * W_up)) * W_down
    """

    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.0) -> None:
        super().__init__()
        self.w_gate = nn.Linear(d_model, d_ff, bias=False)
        self.w_up = nn.Linear(d_model, d_ff, bias=False)
        self.w_down = nn.Linear(d_ff, d_model, bias=False)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Gated activation with element-wise multiplication
        hidden = F.silu(self.w_gate(x)) * self.w_up(x)
        return self.dropout(self.w_down(hidden))


class TransformerBlock(nn.Module):
    """Transformer Decoder Block with Pre-RMSNorm and Residual Connections."""

    def __init__(self, config: NovaConfig) -> None:
        super().__init__()
        self.norm1 = RMSNorm(config.d_model, eps=config.norm_eps)
        self.attn = CausalSelfAttention(config)
        self.norm2 = RMSNorm(config.d_model, eps=config.norm_eps)
        self.ffn = SwiGLU(config.d_model, config.d_ff, dropout=config.dropout)

    def forward(
        self,
        x: torch.Tensor,
        cos: torch.Tensor,
        sin: torch.Tensor,
    ) -> torch.Tensor:
        """Forward pass with pre-normalization and residual addition."""
        x = x + self.attn(self.norm1(x), cos, sin)
        x = x + self.ffn(self.norm2(x))
        return x


class NovaForCausalLM(nn.Module):
    """Nova-Fit Autoregressive Decoder-Only Transformer Language Model.

    Predicts next tokens from input sequences using causal self-attention,
    SwiGLU feed-forward networks, and cross-entropy loss.
    """

    def __init__(self, config: NovaConfig) -> None:
        super().__init__()
        self.config = config

        # Token embeddings
        self.embed_tokens = nn.Embedding(config.vocab_size, config.d_model)

        # Positional rotary embedding
        self.rope = RotaryEmbedding(
            dim=config.head_dim,
            max_seq_len=config.max_seq_len,
            base=config.rope_theta,
        )

        # Transformer blocks
        self.layers = nn.ModuleList(
            [TransformerBlock(config) for _ in range(config.n_layers)]
        )

        # Final normalization and LM projection head
        self.norm_f = RMSNorm(config.d_model, eps=config.norm_eps)
        self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)

        # Optional word embedding weight tying
        if config.tie_word_embeddings:
            self.lm_head.weight = self.embed_tokens.weight

        # Initialize weights with standard normal distribution
        self.apply(self._init_weights)

    def _init_weights(self, module: nn.Module) -> None:
        """Initialize model parameters with normal distribution (mean=0, std=initializer_range)."""
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=self.config.initializer_range)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=self.config.initializer_range)
        elif isinstance(module, RMSNorm):
            nn.init.ones_(module.weight)

    def count_parameters(self, trainable_only: bool = False) -> int:
        """Calculate total number of parameters in the model."""
        if trainable_only:
            return sum(p.numel() for p in self.parameters() if p.requires_grad)
        return sum(p.numel() for p in self.parameters())

    def forward(
        self,
        input_ids: torch.Tensor,
        targets: Optional[torch.Tensor] = None,
    ) -> CausalLMOutput:
        """Execute forward pass and compute optional next-token prediction loss.

        Args:
            input_ids: LongTensor of token IDs with shape [batch_size, seq_len].
            targets: Optional LongTensor with shape [batch_size, seq_len].

        Returns:
            CausalLMOutput with .logits [batch_size, seq_len, vocab_size] and optional .loss.

        Raises:
            TypeError: If input_ids is not a torch.Tensor.
            ValueError: If input tensor dimensions, sequence length, or token IDs are invalid.
        """
        if not isinstance(input_ids, torch.Tensor):
            raise TypeError(
                f"Expected input_ids to be a torch.Tensor, got {type(input_ids).__name__}"
            )

        if input_ids.dim() != 2:
            raise ValueError(
                f"input_ids must be a 2D tensor [batch_size, seq_len], got shape {list(input_ids.shape)}"
            )

        batch_size, seq_len = input_ids.shape

        if seq_len == 0:
            raise ValueError("Sequence length cannot be zero.")

        if seq_len > self.config.max_seq_len:
            raise ValueError(
                f"Input sequence length ({seq_len}) exceeds configured max_seq_len ({self.config.max_seq_len})"
            )

        # Validate token ID ranges defensively
        min_id = input_ids.min().item()
        max_id = input_ids.max().item()
        if min_id < 0 or max_id >= self.config.vocab_size:
            raise ValueError(
                f"Token IDs must be in range [0, {self.config.vocab_size - 1}], "
                f"found min_id={min_id}, max_id={max_id}"
            )

        # Fetch RoPE frequencies for the sequence length
        cos, sin = self.rope(seq_len, input_ids.device)

        # Embed tokens and traverse Transformer layers
        x = self.embed_tokens(input_ids)
        for layer in self.layers:
            x = layer(x, cos, sin)

        x = self.norm_f(x)
        logits = self.lm_head(x)  # [batch_size, seq_len, vocab_size]

        loss = None
        if targets is not None:
            if not isinstance(targets, torch.Tensor):
                raise TypeError(
                    f"Expected targets to be a torch.Tensor, got {type(targets).__name__}"
                )

            if targets.shape != input_ids.shape:
                raise ValueError(
                    f"targets shape {list(targets.shape)} must match input_ids shape {list(input_ids.shape)}"
                )

            # Shift logits and targets for autoregressive next-token prediction
            # logits at position t predict targets at position t+1
            shift_logits = logits[..., :-1, :].contiguous()
            shift_targets = targets[..., 1:].contiguous()

            loss = F.cross_entropy(
                shift_logits.view(-1, self.config.vocab_size),
                shift_targets.view(-1),
                ignore_index=self.config.pad_token_id,
            )

        return CausalLMOutput(logits=logits, loss=loss)


def build_tiny_model(
    config_path: Optional[Union[str, Path]] = None,
    **kwargs: Any,
) -> NovaForCausalLM:
    """Convenience factory to instantiate a tiny Transformer for testing.

    Args:
        config_path: Optional path to JSON configuration file.
        **kwargs: Overrides for configuration parameters.

    Returns:
        Instantiated NovaForCausalLM model with random initialization.
    """
    if config_path is not None:
        config = NovaConfig.from_json_file(config_path)
    else:
        config = NovaConfig()

    if kwargs:
        config_dict = config.to_dict()
        config_dict.update(kwargs)
        config = NovaConfig.from_dict(config_dict)

    return NovaForCausalLM(config)
