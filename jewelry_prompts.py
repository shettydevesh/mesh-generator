def generate_jewelry_prompt(
    item_type: str,
    material: str,
    gemstone: str = None,
    style: str = "photorealistic"
) -> dict:
    """
    Constructs a detailed prompt for Tripo3D jewelry generation (Full Piece).
    Returns a dict with 'prompt', 'negative_prompt', and 'model_settings'.
    """
    base = f"A high-quality 3D model of a {item_type}, made of {material}."
    
    if gemstone:
        base += f" It features a large {gemstone} center stone."
        
    details = (
        "The design should be suitable for 3D printing. "
        "Intricate details, high polish, professional studio lighting, octane render, ray traced. "
        "Isolated object, no background."
    )
    
    full_prompt = f"{base} {style} style. {details}"
    
    return {
        "prompt": full_prompt,
        "negative_prompt": "cartoon, low poly, blurry, flat lighting, drawing, low resolution, artifacts, distorted, noisy",
        "model_settings": {
            "texture_quality": "detailed",
            "geometry_quality": "detailed",
            "pbr": True
        }
    }

def generate_band_prompt(item_type: str, material: str, style: str) -> dict:
    """
    Prompt for just the metal band/base (without the main stone).
    Returns dict with config.
    """
    prompt_text = (
        f"A high-quality 3D model of a {item_type} band/base only, made of {material}. "
        f"{style} style. It has an empty setting/prong ready for a center stone. "
        "Intricate metalwork, high polish, no gems. Isolated object, studio lighting, highly detailed geometry."
    )
    
    return {
        "prompt": prompt_text,
        "negative_prompt": "gemstone, diamond, crystal, low poly, cartoon, blurry, flat",
        "model_settings": {
            "texture_quality": "detailed",
            "geometry_quality": "detailed",
            "pbr": True
        }
    }

def generate_gem_prompt(gem_type: str, cut: str) -> dict:
    """
    Prompt for a standalone gemstone.
    Returns dict with config.
    """
    prompt_text = (
        f"A single loose {gem_type} gemstone, {cut} cut. "
        "High quality, transparent, refracting light, sparkling, caustics, ray tracing. "
        "Isolated object, no background, no metal setting."
    )
    
    return {
        "prompt": prompt_text,
        "negative_prompt": "metal, ring, band, setting, opaque, low poly, cartoon, dark",
        "model_settings": {
            "texture_quality": "detailed",
            "geometry_quality": "detailed",
            "pbr": True
        }
    }
