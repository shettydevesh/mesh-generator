import os
import sys
import asyncio
from tripo_client import TripoWrapper
from mesh_processor import MeshProcessor
from jewelry_prompts import generate_jewelry_prompt, generate_band_prompt, generate_gem_prompt

def get_input(prompt, default=None):
    text = f"{prompt}"
    if default:
        text += f" [{default}]"
    text += ": "
    value = input(text).strip()
    return value if value else default

async def main():
    print("=== Tripo3D Jewelry Generator ===")
    
    # Check for API Key
    if not os.getenv("TRIPO_API_KEY"):
        print("Error: TRIPO_API_KEY not found. Please check your .env file.")
        sys.exit(1)

    tripo = TripoWrapper()
    processor = MeshProcessor()
    
    while True:
        print("\nOptions:")
        print("1. Generate New Jewelry Piece")
        print("2. Segment Existing Model (by Task ID)")
        print("3. Modular Assembly (Separate Band + Stone)")
        print("4. Merge/Process Local Files")
        print("5. Exit")
        
        choice = input("Select option: ")
        
        if choice == "1":
            item = get_input("Item Type (e.g. Ring, Pendant)", "Ring")
            material = get_input("Material", "Gold")
            stone = get_input("Gemstone (optional)", "")
            style = get_input("Style", "Photorealistic")
            
            prompt_data = generate_jewelry_prompt(item, material, stone if stone else None, style)
            prompt_text = prompt_data['prompt']
            
            print(f"\nGenerated Prompt: {prompt_text}")
            if get_input("Proceed with this prompt? (y/n)", "y").lower() != 'y':
                continue
            
            # Unpack additional settings
            gen_kwargs = prompt_data.get('model_settings', {})
            gen_kwargs['negative_prompt'] = prompt_data.get('negative_prompt')
                
            task_id = await tripo.generate_text_to_model(prompt_text, **gen_kwargs)
            if not task_id:
                continue
                
            print(f"Generation Task ID: {task_id}")
            
            result_task = await tripo.wait_for_task(task_id)
            if not result_task:
                continue
            
            # Auto-download base model
            os.makedirs("output", exist_ok=True)
            base_filename = f"output/{task_id}_base.glb"
            model_url = result_task.output.pbr_model or result_task.output.model or result_task.output.base_model
            tripo.download_model(model_url, base_filename)
            
            # Inspect
            print("\nInspecting generated model...")
            processor.inspect_glb(base_filename)
            
            # Ask to segment
            if get_input("Do you want to segment this model? (y/n)", "y").lower() == 'y':
                seg_id = await tripo.segment_model(task_id)
                if seg_id:
                    print(f"Segmentation Task ID: {seg_id}")
                    seg_result = await tripo.wait_for_task(seg_id)
                    if seg_result:
                        # Download segmented model
                        seg_filename = f"output/{task_id}_segmented.glb"
                        tripo.download_model(seg_result.output.model, seg_filename)
                        
                        print("\nInspecting segmented model...")
                        processor.inspect_glb(seg_filename)
                        
                        print("\nSplitting segmented model into parts...")
                        processor.split_scene(seg_filename, "output")
                        
        elif choice == "2":
            tid = get_input("Enter Task ID to segment")
            if tid:
                seg_id = await tripo.segment_model(tid)
                if seg_id:
                    res = await tripo.wait_for_task(seg_id)
                    if res:
                        outfile = f"output/{tid}_segmented.glb"
                        tripo.download_model(res.output.model, outfile)
                        processor.split_scene(outfile, "output")

        elif choice == "3":
            print("\n--- Modular Assembly ---")
            # 1. Generate Band
            item = get_input("Item Type (for band)", "Ring")
            mat = get_input("Band Material", "Gold")
            style = get_input("Style", "Photorealistic")
            band_data = generate_band_prompt(item, mat, style)
            band_prompt = band_data['prompt']
            
            # 2. Generate Stone
            gem = get_input("Gemstone Type", "Diamond")
            cut = get_input("Cut", "Round")
            gem_data = generate_gem_prompt(gem, cut)
            gem_prompt = gem_data['prompt']
            
            print(f"\nBand Prompt: {band_prompt}")
            print(f"Gem Prompt: {gem_prompt}")
            
            if get_input("Proceed? (y/n)", "y").lower() != 'y':
                continue
                
            print("\nGenerating Band...")
            band_kwargs = band_data.get('model_settings', {})
            band_kwargs['negative_prompt'] = band_data.get('negative_prompt')
            band_id = await tripo.generate_text_to_model(band_prompt, **band_kwargs)
            
            print("\nGenerating Gemstone...")
            gem_kwargs = gem_data.get('model_settings', {})
            gem_kwargs['negative_prompt'] = gem_data.get('negative_prompt')
            gem_id = await tripo.generate_text_to_model(gem_prompt, **gem_kwargs)
            
            if band_id and gem_id:
                print(f"\nWaiting for Band ({band_id})...")
                band_res = await tripo.wait_for_task(band_id)
                
                print(f"\nWaiting for Gem ({gem_id})...")
                gem_res = await tripo.wait_for_task(gem_id)
                
                os.makedirs("output", exist_ok=True)
                if band_res and gem_res:
                    band_url = band_res.output.pbr_model or band_res.output.model
                    gem_url = gem_res.output.pbr_model or gem_res.output.model
                    
                    band_file = f"output/{band_id}_band.glb"
                    gem_file = f"output/{gem_id}_gem.glb"
                    
                    await asyncio.to_thread(tripo.download_model, band_url, band_file)
                    await asyncio.to_thread(tripo.download_model, gem_url, gem_file)
                    
                    print(f"\nParts saved to:\n- {band_file}\n- {gem_file}")
                    
                    if get_input("Merge parts into one file? (y/n)", "n").lower() == 'y':
                        # Merge
                        final_file = f"output/assembled_{band_id}_{gem_id}.glb"
                        print("\nMerging parts...")
                        
                        # Default positioning: Gem slightly raised/centered?
                        # Since we don't know exact scale, we just place them at 0,0,0
                        parts = [
                            {'path': band_file, 'position': [0, 0, 0]},
                            {'path': gem_file, 'position': [0, 0, 0]} 
                        ]
                        processor.merge_meshes(parts, final_file)

        elif choice == "4":
            print("Feature to merge local files (Implementation pending CLI args)")
            # Stub for manual merge if needed
            
        elif choice == "5":
            break
            
if __name__ == "__main__":
    asyncio.run(main())
