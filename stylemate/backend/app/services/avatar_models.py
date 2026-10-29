"""Fitting-room avatar models: the GLB files in frontend/models.

Drop a .glb into that folder and the fitting room offers it - no code to edit.
Each file's category (male / female / other) comes from an optional
models.json in the same folder, else from its name ("female" is checked before
"male", since one contains the other). The folder is read on every request, so
a new file appears on a running local server without a restart; on a host it
arrives with the next deploy.

Every file is checked before it is offered: a real GLB 2.0 header whose length
matches the file, a JSON chunk that parses, no required extension this
project's GLTFLoader cannot decode (Draco, Meshopt, KTX2/Basis are not set up),
and no external .bin or image files that are missing. Anything that fails is
reported under "errors" with the reason, never offered to the viewer.
"""
from __future__ import annotations

import json
import mimetypes
import os
import re
import struct
from pathlib import Path

# Served as model/gltf-binary rather than text/plain (Python does not know .glb).
mimetypes.add_type("model/gltf-binary", ".glb")

MODELS_DIR = Path(os.getenv("SM_MODELS_DIR")
                  or Path(__file__).resolve().parents[3] / "frontend" / "models")
REGISTRY = "models.json"
MAX_BYTES = 80 * 1024 * 1024          # a larger avatar would be too slow to download anyway

# Required extensions that three r169's GLTFLoader handles with no extra decoder.
SUPPORTED_REQUIRED = {
    "KHR_materials_unlit", "KHR_materials_emissive_strength", "KHR_materials_ior",
    "KHR_materials_specular", "KHR_materials_transmission", "KHR_materials_volume",
    "KHR_materials_clearcoat", "KHR_materials_sheen", "KHR_materials_iridescence",
    "KHR_materials_anisotropy", "KHR_materials_dispersion", "KHR_texture_transform",
    "KHR_mesh_quantization", "KHR_lights_punctual", "EXT_texture_webp",
    "EXT_mesh_gpu_instancing",
}
MODEL_LIKE = {".gltf", ".fbx", ".obj", ".usdz", ".blend", ".vrm"}


def _category(stem: str) -> str:
    s = stem.lower()
    if re.search(r"female|woman|women|girl", s):
        return "female"
    if re.search(r"male|man|men|boy", s):
        return "male"
    return "other"


def _pretty(stem: str) -> str:
    words = re.sub(r"[_\-]+", " ", stem).strip()
    return words[:1].upper() + words[1:]


def _check_glb(path: Path) -> tuple[bool, str]:
    """(ok, reason). Reads only the 12-byte header and the JSON chunk."""
    size = path.stat().st_size
    if size < 20:
        return False, "file is empty or truncated"
    if size > MAX_BYTES:
        return False, f"file is {size // (1024 * 1024)} MB; the limit is {MAX_BYTES // (1024 * 1024)} MB"
    with path.open("rb") as f:
        magic, version, length = struct.unpack("<4sII", f.read(12))
        if magic != b"glTF":
            return False, "not a GLB file (no glTF header)"
        if version != 2:
            return False, f"glTF version {version}; only 2.0 is supported"
        if length != size:
            return False, f"header says {length} bytes but the file has {size} - truncated or corrupt"
        clen, ctype = struct.unpack("<I4s", f.read(8))
        if ctype != b"JSON":
            return False, "first chunk is not JSON"
        try:
            doc = json.loads(f.read(clen))
        except ValueError:
            return False, "the JSON chunk does not parse"
    if not doc.get("meshes"):
        return False, "contains no meshes"
    unsupported = sorted(set(doc.get("extensionsRequired") or []) - SUPPORTED_REQUIRED)
    if unsupported:
        return False, "needs " + ", ".join(unsupported) + ", which this viewer cannot decode"
    for kind in ("buffers", "images"):
        for item in doc.get(kind) or []:
            uri = item.get("uri")
            if uri and not uri.startswith("data:") and not (path.parent / uri).exists():
                return False, f"refers to an external file that is missing: {uri}"
    return True, ""


def _registry(folder: Path) -> tuple[dict[str, dict], str]:
    """{file: entry} from models.json, and an error message if it is unusable."""
    p = folder / REGISTRY
    if not p.exists():
        return {}, ""
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        items = data.get("models", data) if isinstance(data, dict) else data
        return {str(e["file"]): e for e in items if isinstance(e, dict) and e.get("file")}, ""
    except (ValueError, KeyError, TypeError) as e:
        return {}, f"{REGISTRY} could not be read ({e}); using file names instead"


def list_models() -> dict:
    folder = MODELS_DIR
    out: dict = {"dir": "frontend/models", "models": [], "errors": [], "registry": False}
    if not folder.is_dir():
        out["note"] = "No models folder - the fitting room uses the basic avatar."
        return out
    reg, reg_err = _registry(folder)
    out["registry"] = bool(reg)
    if reg_err:
        out["errors"].append({"file": REGISTRY, "reason": reg_err})
    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.name.startswith("."):
            continue
        ext = path.suffix.lower()
        if ext != ".glb":
            if ext in MODEL_LIKE:
                out["errors"].append({"file": path.name, "reason": f"{ext} is not supported; export it as .glb"})
            continue
        ok, why = _check_glb(path)
        if not ok:
            out["errors"].append({"file": path.name, "reason": why})
            continue
        meta = reg.get(path.name, {})
        cat = str(meta.get("category") or _category(path.stem)).lower()
        out["models"].append({
            "id": str(meta.get("id") or path.stem),
            "name": str(meta.get("name") or _pretty(path.stem)),
            "category": cat if cat in ("male", "female") else "other",
            "file": path.name,
            "url": "models/" + path.name,
            "bytes": path.stat().st_size,
            "default": bool(meta.get("default")),
            "rotationY": float(meta.get("rotationY") or 0),
        })
    if not out["models"]:
        out["note"] = "No usable .glb files - the fitting room uses the basic avatar."
    return out
