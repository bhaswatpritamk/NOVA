"""Nova-Fit Tokenizer Implementation.

Provides byte-level Byte Pair Encoding (BPE) tokenizer training, encoding,
decoding, serialization, and explicit special token handling for Project Nova-Fit.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Collection, Dict, List, Optional, Sequence, Union

import tokenizers
from tokenizers import Tokenizer, decoders, models, pre_tokenizers, trainers

# Standard special tokens for Nova-Fit decoder-only Transformer
DEFAULT_SPECIAL_TOKENS = ["<pad>", "<unk>", "<bos>", "<eos>"]
DEFAULT_SPECIAL_TOKENS_MAP = {
    "pad_token": "<pad>",
    "unk_token": "<unk>",
    "bos_token": "<bos>",
    "eos_token": "<eos>",
}


def compute_file_sha256(file_path: Union[str, Path]) -> str:
    """Compute the SHA-256 cryptographic digest of a file.

    Args:
        file_path: Path to target file.

    Returns:
        Hexadecimal SHA-256 digest string.
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Cannot compute hash; file does not exist: {path}")

    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


@dataclass
class TokenizerMetadata:
    """Detailed reproducibility metadata recorded during tokenizer training."""

    algorithm: str
    target_vocab_size: int
    actual_vocab_size: int
    special_tokens: Dict[str, Dict[str, Union[str, int]]]
    corpus_path: str
    corpus_sha256: Optional[str]
    dependency_version: str
    python_version: str
    training_config: Dict[str, Any]
    created_at: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to JSON-serializable dictionary."""
        return asdict(self)


class NovaTokenizer:
    """Nova-Fit Byte-Level BPE Tokenizer.

    Wraps the Hugging Face tokenizers backend to provide strict input validation,
    explicit special-token handling (preventing accidental tokenization of reserved
    strings in ordinary text), round-trip fidelity, and metadata serialization.
    """

    def __init__(
        self,
        hf_tokenizer: Tokenizer,
        special_tokens_map: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize NovaTokenizer.

        Args:
            hf_tokenizer: Underlying Hugging Face Tokenizer instance.
            special_tokens_map: Optional mapping of special token roles
                (e.g., 'pad_token') to token strings (e.g., '<pad>').
            metadata: Optional dictionary of training/provenance metadata.
        """
        if not isinstance(hf_tokenizer, Tokenizer):
            raise TypeError(
                f"Expected hf_tokenizer to be an instance of tokenizers.Tokenizer, "
                f"got {type(hf_tokenizer).__name__}"
            )

        self._tokenizer = hf_tokenizer
        self._special_tokens_map = dict(special_tokens_map or DEFAULT_SPECIAL_TOKENS_MAP)
        self._metadata = dict(metadata or {})

        # Validate and cache special token IDs
        self._special_token_ids: Dict[str, int] = {}
        for role, token_str in self._special_tokens_map.items():
            tok_id = self._tokenizer.token_to_id(token_str)
            if tok_id is not None:
                self._special_token_ids[role] = tok_id
                self._special_token_ids[token_str] = tok_id

    # -------------------------------------------------------------------------
    # Properties & Vocabulary Access
    # -------------------------------------------------------------------------

    @property
    def hf_tokenizer(self) -> Tokenizer:
        """Access underlying Hugging Face Tokenizer instance."""
        return self._tokenizer

    @property
    def vocab_size(self) -> int:
        """Return total vocabulary size including special tokens."""
        return self._tokenizer.get_vocab_size()

    def __len__(self) -> int:
        """Return total vocabulary size."""
        return self.vocab_size

    def get_vocab(self) -> Dict[str, int]:
        """Return copy of full vocabulary mapping token strings to IDs."""
        return self._tokenizer.get_vocab()

    def token_to_id(self, token: str) -> Optional[int]:
        """Return token ID for given string token, or None if not found."""
        if not isinstance(token, str):
            raise TypeError(f"Token must be str, got {type(token).__name__}")
        return self._tokenizer.token_to_id(token)

    def id_to_token(self, token_id: int) -> Optional[str]:
        """Return string token for given token ID, or None if out of bounds."""
        if not isinstance(token_id, int):
            raise TypeError(f"Token ID must be int, got {type(token_id).__name__}")
        return self._tokenizer.id_to_token(token_id)

    @property
    def metadata(self) -> Dict[str, Any]:
        """Return dictionary of training and configuration metadata."""
        return dict(self._metadata)

    # -------------------------------------------------------------------------
    # Special Tokens Access
    # -------------------------------------------------------------------------

    @property
    def special_tokens_map(self) -> Dict[str, str]:
        """Return mapping of special token roles to token strings."""
        return dict(self._special_tokens_map)

    @property
    def special_token_ids(self) -> Dict[str, int]:
        """Return mapping of role names and token strings to their IDs."""
        return dict(self._special_token_ids)

    @property
    def pad_token(self) -> str:
        """Return padding token string."""
        return self._special_tokens_map.get("pad_token", "<pad>")

    @property
    def pad_token_id(self) -> int:
        """Return padding token ID."""
        tok_id = self.token_to_id(self.pad_token)
        if tok_id is None:
            raise KeyError(f"Padding token '{self.pad_token}' not found in vocabulary.")
        return tok_id

    @property
    def unk_token(self) -> Optional[str]:
        """Return unknown token string, if configured."""
        return self._special_tokens_map.get("unk_token")

    @property
    def unk_token_id(self) -> Optional[int]:
        """Return unknown token ID, or None if not configured."""
        if self.unk_token is None:
            return None
        return self.token_to_id(self.unk_token)

    @property
    def eos_token(self) -> str:
        """Return end-of-text token string."""
        return self._special_tokens_map.get("eos_token", "<eos>")

    @property
    def eos_token_id(self) -> int:
        """Return end-of-text token ID."""
        tok_id = self.token_to_id(self.eos_token)
        if tok_id is None:
            raise KeyError(f"End-of-text token '{self.eos_token}' not found in vocabulary.")
        return tok_id

    @property
    def bos_token(self) -> Optional[str]:
        """Return beginning-of-text token string, if configured."""
        return self._special_tokens_map.get("bos_token")

    @property
    def bos_token_id(self) -> Optional[int]:
        """Return beginning-of-text token ID, or None if not configured."""
        if self.bos_token is None:
            return None
        return self.token_to_id(self.bos_token)

    def get_special_token_id(self, identifier: str) -> int:
        """Retrieve token ID for special token by role name or string content.

        Args:
            identifier: Role name (e.g., 'pad_token', 'pad') or token string
                (e.g., '<pad>').

        Returns:
            Integer token ID.

        Raises:
            KeyError: If identifier does not match any configured special token.
        """
        if not isinstance(identifier, str):
            raise TypeError(f"Special token identifier must be str, got {type(identifier).__name__}")

        # Check direct lookup in cached special token IDs
        if identifier in self._special_token_ids:
            return self._special_token_ids[identifier]

        # Check role alias without '_token' suffix
        with_suffix = f"{identifier}_token"
        if with_suffix in self._special_token_ids:
            return self._special_token_ids[with_suffix]

        # Fallback to direct token_to_id check
        tok_id = self.token_to_id(identifier)
        if tok_id is not None:
            return tok_id

        raise KeyError(
            f"Special token identifier '{identifier}' not found in configured special tokens: "
            f"{list(self._special_tokens_map.keys())} or {list(self._special_tokens_map.values())}"
        )

    # -------------------------------------------------------------------------
    # Encoding & Decoding
    # -------------------------------------------------------------------------

    def encode(
        self,
        text: str,
        allow_special: Union[bool, Collection[str]] = False,
    ) -> List[int]:
        """Encode text string into a list of integer token IDs.

        Explicit Special-Token Handling:
        By default (allow_special=False), ordinary input text is strictly
        encoded as standard subwords/bytes. If the text literally contains
        a reserved string such as '<pad>' or '<eos>', it is parsed into
        constituent byte tokens, NEVER yielding the special token ID.
        This prevents accidental token injection or parsing collisions.

        If allow_special is True, all configured special tokens are parsed as
        their reserved token IDs.
        If allow_special is a collection of strings, only those specified
        special tokens are recognized, and other special tokens cause a
        ValueError.

        Args:
            text: Input string to tokenize.
            allow_special: Boolean flag or collection of allowed special tokens.

        Returns:
            List of integer token IDs.

        Raises:
            TypeError: If input text is not a string.
            ValueError: If an unallowed special token is present when a
                restricted collection is supplied.
        """
        if not isinstance(text, str):
            raise TypeError(
                f"Expected str input for text, but got {type(text).__name__} ({text!r})"
            )

        if not text:
            return []

        # Handle explicit special token permission
        if allow_special is False:
            # In tokenizers library, setting encode_special_tokens = True instructs
            # the tokenizer to treat special tokens as ordinary text strings to be encoded.
            self._tokenizer.encode_special_tokens = True
            encoding = self._tokenizer.encode(text)
            return encoding.ids
        elif allow_special is True:
            # Setting encode_special_tokens = False allows the tokenizer to match
            # special tokens against the added vocabulary.
            self._tokenizer.encode_special_tokens = False
            encoding = self._tokenizer.encode(text)
            return encoding.ids
        elif isinstance(allow_special, (set, list, tuple, frozenset)):
            # Check for disallowed special tokens
            allowed_set = set(allow_special)
            configured_specials = set(self._special_tokens_map.values())
            disallowed = configured_specials - allowed_set

            for token_str in disallowed:
                if token_str in text:
                    raise ValueError(
                        f"Encountered disallowed special token '{token_str}' in input text. "
                        f"Allowed special tokens: {sorted(allowed_set)}"
                    )

            self._tokenizer.encode_special_tokens = False
            encoding = self._tokenizer.encode(text)
            return encoding.ids
        else:
            raise TypeError(
                f"allow_special must be bool or Collection[str], got {type(allow_special).__name__}"
            )

    def encode_batch(
        self,
        texts: List[str],
        allow_special: Union[bool, Collection[str]] = False,
    ) -> List[List[int]]:
        """Encode a batch of text strings into token ID lists.

        Args:
            texts: List of strings.
            allow_special: Special token permission policy.

        Returns:
            List of token ID lists.
        """
        if not isinstance(texts, list):
            raise TypeError(f"texts must be a list of strings, got {type(texts).__name__}")
        return [self.encode(text, allow_special=allow_special) for text in texts]

    def decode(
        self,
        ids: Sequence[int],
        skip_special_tokens: bool = False,
    ) -> str:
        """Decode a sequence of token IDs back into an exact text string.

        Args:
            ids: Sequence of integer token IDs.
            skip_special_tokens: If True, special tokens are omitted from output.

        Returns:
            Decoded string.

        Raises:
            TypeError: If ids is not a sequence or contains non-integer values.
            ValueError: If any token ID is negative or >= vocab_size.
        """
        if not isinstance(ids, (list, tuple)):
            raise TypeError(f"Expected sequence of token IDs (list/tuple), got {type(ids).__name__}")

        if not ids:
            return ""

        vocab_limit = self.vocab_size
        for idx, token_id in enumerate(ids):
            # Check integer type (and not bool, since bool subclasses int in Python)
            if not isinstance(token_id, int) or isinstance(token_id, bool):
                raise TypeError(
                    f"All token IDs must be integers; found {type(token_id).__name__} "
                    f"at index {idx}: {token_id!r}"
                )
            if token_id < 0 or token_id >= vocab_limit:
                raise ValueError(
                    f"Token ID {token_id} at index {idx} is out of bounds for "
                    f"vocabulary size {vocab_limit} (valid range: 0 to {vocab_limit - 1})."
                )

        return self._tokenizer.decode(list(ids), skip_special_tokens=skip_special_tokens)

    def decode_batch(
        self,
        batch_ids: List[Sequence[int]],
        skip_special_tokens: bool = False,
    ) -> List[str]:
        """Decode a batch of token ID sequences.

        Args:
            batch_ids: List of token ID sequences.
            skip_special_tokens: If True, special tokens are omitted.

        Returns:
            List of decoded strings.
        """
        if not isinstance(batch_ids, list):
            raise TypeError(f"batch_ids must be a list of sequences, got {type(batch_ids).__name__}")
        return [self.decode(seq, skip_special_tokens=skip_special_tokens) for seq in batch_ids]

    # -------------------------------------------------------------------------
    # Training Factory
    # -------------------------------------------------------------------------

    @classmethod
    def train_from_corpus(
        cls,
        corpus_path: Union[str, Path, Sequence[Union[str, Path]]],
        vocab_size: int = 8000,
        min_frequency: int = 1,
        special_tokens: Optional[Sequence[str]] = None,
        special_tokens_map: Optional[Dict[str, str]] = None,
        add_prefix_space: bool = False,
        trim_offsets: bool = True,
    ) -> NovaTokenizer:
        """Train a byte-level BPE tokenizer from scratch on a text corpus.

        Args:
            corpus_path: Path to text file or sequence of file paths.
            vocab_size: Target vocabulary size (provisional production target: 8000).
            min_frequency: Minimum pair occurrence frequency to merge.
            special_tokens: Explicit list of special tokens.
            special_tokens_map: Role mapping for special tokens.
            add_prefix_space: Whether to insert prefix space before words.
            trim_offsets: Whether to trim whitespace offsets in tokens.

        Returns:
            Instantiated and trained NovaTokenizer.

        Raises:
            FileNotFoundError: If corpus path does not exist.
            ValueError: If vocab_size or min_frequency are non-positive.
            TypeError: If input arguments have invalid types.
        """
        if not isinstance(vocab_size, int) or vocab_size <= 0:
            raise ValueError(f"Target vocab_size must be a positive integer, got {vocab_size}")
        if not isinstance(min_frequency, int) or min_frequency <= 0:
            raise ValueError(f"min_frequency must be a positive integer, got {min_frequency}")

        # Normalize corpus paths
        paths: List[Path] = []
        if isinstance(corpus_path, (str, Path)):
            p = Path(corpus_path)
            if not p.is_file():
                raise FileNotFoundError(f"Corpus file not found: {p}")
            paths.append(p)
        elif isinstance(corpus_path, (list, tuple)):
            for cp in corpus_path:
                p = Path(cp)
                if not p.is_file():
                    raise FileNotFoundError(f"Corpus file not found: {p}")
                paths.append(p)
        else:
            raise TypeError(
                f"corpus_path must be str, Path, or Sequence of paths, got {type(corpus_path).__name__}"
            )

        if not paths:
            raise ValueError("No corpus files provided for training.")

        # Compute SHA-256 hash of primary corpus file
        primary_hash = compute_file_sha256(paths[0]) if len(paths) == 1 else None

        specials = list(special_tokens or DEFAULT_SPECIAL_TOKENS)
        roles = dict(special_tokens_map or DEFAULT_SPECIAL_TOKENS_MAP)

        # Ensure all mapped tokens are in specials list
        for tok in roles.values():
            if tok not in specials:
                specials.append(tok)

        # Build Byte-Level BPE Tokenizer pipeline
        unk_token = roles.get("unk_token", "<unk>")
        bpe_model = models.BPE(unk_token=unk_token)
        tok = Tokenizer(bpe_model)

        tok.pre_tokenizer = pre_tokenizers.ByteLevel(
            add_prefix_space=add_prefix_space,
            trim_offsets=trim_offsets,
        )
        tok.decoder = decoders.ByteLevel()

        # Trainer setup with byte-level alphabet to guarantee coverage of all 256 bytes
        trainer = trainers.BpeTrainer(
            vocab_size=vocab_size,
            min_frequency=min_frequency,
            special_tokens=specials,
            initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
        )

        # Execute training on corpus files
        file_paths_str = [str(p) for p in paths]
        tok.train(file_paths_str, trainer=trainer)

        actual_vocab_size = tok.get_vocab_size()

        # Build structured special tokens record
        special_tokens_record: Dict[str, Dict[str, Union[str, int]]] = {}
        for role, tok_str in roles.items():
            tok_id = tok.token_to_id(tok_str)
            if tok_id is not None:
                special_tokens_record[role] = {"token": tok_str, "id": tok_id}

        metadata = TokenizerMetadata(
            algorithm="byte_level_bpe",
            target_vocab_size=vocab_size,
            actual_vocab_size=actual_vocab_size,
            special_tokens=special_tokens_record,
            corpus_path=str(paths[0]) if len(paths) == 1 else str(file_paths_str),
            corpus_sha256=primary_hash,
            dependency_version=f"tokenizers=={tokenizers.__version__}",
            python_version=sys.version.split()[0],
            training_config={
                "vocab_size": vocab_size,
                "min_frequency": min_frequency,
                "add_prefix_space": add_prefix_space,
                "trim_offsets": trim_offsets,
                "special_tokens": specials,
            },
            created_at=datetime.now(timezone.utc).isoformat(),
        ).to_dict()

        return cls(
            hf_tokenizer=tok,
            special_tokens_map=roles,
            metadata=metadata,
        )

    # -------------------------------------------------------------------------
    # Serialization & Deserialization
    # -------------------------------------------------------------------------

    def save(
        self,
        output_path: Union[str, Path],
        save_metadata: bool = True,
    ) -> Dict[str, Path]:
        """Save the tokenizer and metadata to disk.

        Args:
            output_path: Directory path or path to JSON file. If directory,
                saves 'tokenizer.json' and 'tokenizer_metadata.json' inside it.
            save_metadata: Whether to write companion metadata JSON file.

        Returns:
            Dictionary mapping asset names ('tokenizer', 'metadata') to Path objects.
        """
        target = Path(output_path)
        if target.suffix == ".json":
            out_dir = target.parent
            tok_file = target
            meta_file = target.with_name(f"{target.stem}_metadata.json")
        else:
            out_dir = target
            tok_file = out_dir / "tokenizer.json"
            meta_file = out_dir / "tokenizer_metadata.json"

        out_dir.mkdir(parents=True, exist_ok=True)

        # Save Hugging Face tokenizer definition
        self._tokenizer.save(str(tok_file))

        # Update metadata actual vocab and special tokens dynamically
        saved_files = {"tokenizer": tok_file}
        if save_metadata:
            meta = dict(self._metadata)
            meta["actual_vocab_size"] = self.vocab_size

            # Ensure special tokens map and IDs are recorded
            special_record: Dict[str, Dict[str, Union[str, int]]] = {}
            for role, tok_str in self._special_tokens_map.items():
                tok_id = self.token_to_id(tok_str)
                if tok_id is not None:
                    special_record[role] = {"token": tok_str, "id": tok_id}
            meta["special_tokens"] = special_record

            with open(meta_file, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)
            saved_files["metadata"] = meta_file

        return saved_files

    @classmethod
    def from_file(
        cls,
        path: Union[str, Path],
        special_tokens_map: Optional[Dict[str, str]] = None,
    ) -> NovaTokenizer:
        """Load a saved NovaTokenizer from a file or directory.

        Args:
            path: Path to tokenizer.json file or directory containing it.
            special_tokens_map: Optional override for special token role mapping.

        Returns:
            Instantiated NovaTokenizer.

        Raises:
            FileNotFoundError: If tokenizer file does not exist.
        """
        p = Path(path)
        if p.is_dir():
            tok_file = p / "tokenizer.json"
            meta_file = p / "tokenizer_metadata.json"
        elif p.is_file():
            tok_file = p
            meta_file = p.with_name(f"{p.stem}_metadata.json")
            if not meta_file.exists():
                meta_file = p.parent / "tokenizer_metadata.json"
        else:
            raise FileNotFoundError(f"Path does not exist: {p}")

        if not tok_file.is_file():
            raise FileNotFoundError(f"Tokenizer definition file not found: {tok_file}")

        hf_tok = Tokenizer.from_file(str(tok_file))

        # Load metadata if present
        metadata: Dict[str, Any] = {}
        if meta_file.is_file():
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
            except Exception:
                metadata = {}

        # Reconstruct special token roles from metadata if available
        roles = dict(special_tokens_map or {})
        if not roles and "special_tokens" in metadata:
            for role, data in metadata["special_tokens"].items():
                if isinstance(data, dict) and "token" in data:
                    roles[role] = data["token"]

        return cls(
            hf_tokenizer=hf_tok,
            special_tokens_map=roles or None,
            metadata=metadata or None,
        )


# -----------------------------------------------------------------------------
# Module-level convenience functions
# -----------------------------------------------------------------------------


def train_tokenizer(
    corpus_path: Union[str, Path, Sequence[Union[str, Path]]],
    vocab_size: int = 8000,
    min_frequency: int = 1,
    special_tokens: Optional[Sequence[str]] = None,
    special_tokens_map: Optional[Dict[str, str]] = None,
) -> NovaTokenizer:
    """Convenience function to train a NovaTokenizer from a corpus path."""
    return NovaTokenizer.train_from_corpus(
        corpus_path=corpus_path,
        vocab_size=vocab_size,
        min_frequency=min_frequency,
        special_tokens=special_tokens,
        special_tokens_map=special_tokens_map,
    )


def load_tokenizer(path: Union[str, Path]) -> NovaTokenizer:
    """Convenience function to load a NovaTokenizer from disk."""
    return NovaTokenizer.from_file(path)


def encode(text: str, tokenizer: NovaTokenizer, allow_special: bool = False) -> List[int]:
    """Convenience function to encode text using a NovaTokenizer."""
    return tokenizer.encode(text, allow_special=allow_special)


def decode(ids: Sequence[int], tokenizer: NovaTokenizer, skip_special_tokens: bool = False) -> str:
    """Convenience function to decode token IDs using a NovaTokenizer."""
    return tokenizer.decode(ids, skip_special_tokens=skip_special_tokens)
