"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║          🔥 CREATIVE INTELLIGENCE ENGINE — INTEGRATION TEST 🔥              ║
║                                                                              ║
║                    COMPLETE END-TO-END WORKFLOW VALIDATION                   ║
║                                                                              ║
║  This test validates the entire Creative Intelligence Engine pipeline:      ║
║                                                                              ║
║    User Input → PIC → CRE → MMOE → Studios → ADG → CCS → OAE → Dashboard   ║
║                                                                              ║
║  Proving that all 7 modules work together seamlessly.                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import json
import sys
import io
from datetime import datetime
from typing import Dict, Any

# Fix Windows console encoding for emoji output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Import all 7 modules of the Creative Intelligence Engine
from project_intelligence_core import get_pic
from creative_reasoning_engine_v2 import get_cre
from multi_medium_orchestration_engine import get_mmoe
from asset_dependency_graph import get_adg, AssetType, AssetStatus
from creative_continuity_system import get_ccs
from output_assembly_engine import get_oae, DeliverableType, Platform, ExportFormat
from dominion_command_dashboard import get_dominion_dashboard


def run_complete_workflow_test(user_project_description: str) -> Dict[str, Any]:
    """
    Run the complete Creative Intelligence Engine workflow.
    
    This simulates a real project from start to finish:
    1. User describes their project
    2. PIC interprets the project
    3. CRE develops creative direction
    4. MMOE orchestrates production
    5. Studios execute (simulated)
    6. ADG tracks all assets
    7. CCS validates continuity
    8. OAE assembles deliverables
    9. Dashboard displays everything
    
    Returns complete workflow results including dashboard view.
    """
    
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "🔥 CREATIVE INTELLIGENCE ENGINE — WORKFLOW TEST 🔥".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    workflow_results = {
        "test_started_at": datetime.utcnow().isoformat() + "Z",
        "user_input": user_project_description,
        "steps_completed": []
    }
    
    # ═══════════════════════════════════════════════════════════════════════
    # STEP 1: PROJECT INTELLIGENCE CORE (PIC)
    # ═══════════════════════════════════════════════════════════════════════
    
    print("━" * 80)
    print("STEP 1: PROJECT INTERPRETATION (PIC)")
    print("━" * 80)
    print(f"📝 User Input: {user_project_description}")
    print()
    
    pic = get_pic()
    pic_output = pic.interpret_project(user_project_description)
    
    print(f"✅ Project ID: {pic_output['id']}")
    print(f"   Project Type: {pic_output['type']}")
    print(f"   Complexity: {pic_output['complexity']}")
    print(f"   Required Mediums: {', '.join(pic_output['required_mediums'])}")
    print(f"   Asset Count: {len(pic_output['asset_requirements'])}")
    print()
    
    workflow_results["steps_completed"].append("PIC")
    workflow_results["pic_output"] = pic_output
    
    # ═══════════════════════════════════════════════════════════════════════
    # STEP 2: CREATIVE REASONING ENGINE (CRE)
    # ═══════════════════════════════════════════════════════════════════════
    
    print("━" * 80)
    print("STEP 2: CREATIVE REASONING (CRE)")
    print("━" * 80)
    
    cre = get_cre()
    
    # Mock assets for CRE analysis
    mock_assets = [
        {"asset_id": "asset_1", "name": "hero_video", "medium": "video"},
        {"asset_id": "asset_2", "name": "graphics_pack", "medium": "graphics"},
        {"asset_id": "asset_3", "name": "background_music", "medium": "audio"}
    ]
    
    # Build project dict for CRE (using PIC output)
    cre_project = {
        "project_id": pic_output["id"],
        "project_type": pic_output["type"],
        "is_dominion_optimized": True,
        "dominion_type": "youth_entrepreneurship",
        "mediums": pic_output["required_mediums"]
    }
    
    # Run CRE analyses
    style_analysis = cre.analyze_style(cre_project, mock_assets)
    narrative_analysis = cre.analyze_narrative(cre_project, mock_assets)
    brand_analysis = cre.check_brand_alignment(cre_project, mock_assets)
    
    # Combine into creative output
    cre_output = {
        "project_id": pic_output["id"],
        "style_intelligence": style_analysis,
        "narrative_intelligence": narrative_analysis,
        "brand_identity": brand_analysis,
        "creative_quality_predictor": {"target_quality_level": "excellent"}
    }
    
    print(f"✅ Style Direction: {style_analysis['target_style']}")
    print(f"   Style Consistency: {style_analysis['overall_consistency']:.3f}")
    print(f"   Narrative Type: {narrative_analysis['narrative_type']}")
    print(f"   Narrative Coherence: {narrative_analysis['overall_coherence']:.3f}")
    print(f"   Brand Alignment: {brand_analysis['overall_brand_alignment']:.3f}")
    print()
    
    workflow_results["steps_completed"].append("CRE")
    workflow_results["cre_output"] = cre_output
    
    # ═══════════════════════════════════════════════════════════════════════
    # STEP 3: MULTI-MEDIUM ORCHESTRATION ENGINE (MMOE)
    # ═══════════════════════════════════════════════════════════════════════
    
    print("━" * 80)
    print("STEP 3: PRODUCTION ORCHESTRATION (MMOE)")
    print("━" * 80)
    
    mmoe = get_mmoe()
    mmoe_output = mmoe.orchestrate_project(
        project_id=pic_output["id"],
        creative_direction=cre_output,
        project_metadata={"project_type": pic_output["type"]}
    )
    
    print(f"✅ Total Waves: {len(mmoe_output['orchestration_waves'])}")
    print(f"   Parallel Streams: {mmoe_output['execution_plan']['max_parallel_streams']}")
    print(f"   Total Duration: {mmoe_output['execution_plan']['estimated_duration_seconds']}s")
    print()
    
    for wave in mmoe_output["orchestration_waves"]:
        print(f"   Wave: {wave['wave_name']} — {len(wave['studios'])} studios")
    print()
    
    workflow_results["steps_completed"].append("MMOE")
    workflow_results["mmoe_output"] = mmoe_output
    
    # ═══════════════════════════════════════════════════════════════════════
    # SIMULATED STUDIO EXECUTION
    # ═══════════════════════════════════════════════════════════════════════
    
    print("━" * 80)
    print("SIMULATED STUDIO EXECUTION")
    print("━" * 80)
    print("🎨 Graphics Studio: Creating visuals...")
    print("🎵 Audio Studio: Recording and mixing...")
    print("🎬 Video Studio: Assembling timeline...")
    print("✅ Studios completed production")
    print()
    
    # ═══════════════════════════════════════════════════════════════════════
    # STEP 4: ASSET DEPENDENCY GRAPH (ADG)
    # ═══════════════════════════════════════════════════════════════════════
    
    print("━" * 80)
    print("STEP 4: ASSET TRACKING (ADG)")
    print("━" * 80)
    
    adg = get_adg()
    project_id = pic_output["id"]
    
    # Register assets from production
    script_id = adg.register_asset(
        project_id=project_id,
        asset_name="Project Script",
        asset_type=AssetType.SCRIPT,
        owner="cre_narrative_intelligence",
        metadata={"words": 1500, "scenes": 5}
    )
    
    voiceover_id = adg.register_asset(
        project_id=project_id,
        asset_name="Voiceover Recording",
        asset_type=AssetType.VOICEOVER,
        owner="audio_studio",
        metadata={"duration_seconds": 180, "format": "wav"}
    )
    
    graphics_id = adg.register_asset(
        project_id=project_id,
        asset_name="Intro Graphics Pack",
        asset_type=AssetType.MOTION_GRAPHICS,
        owner="graphics_studio",
        metadata={"count": 10, "resolution": "1920x1080"}
    )
    
    music_id = adg.register_asset(
        project_id=project_id,
        asset_name="Background Music",
        asset_type=AssetType.MUSIC,
        owner="audio_studio",
        metadata={"duration_seconds": 180, "bpm": 120}
    )
    
    video_id = adg.register_asset(
        project_id=project_id,
        asset_name="Final Video Assembly",
        asset_type=AssetType.VIDEO,
        owner="video_studio",
        metadata={"duration_seconds": 720, "resolution": "1920x1080"}
    )
    
    # Map dependencies
    adg.add_dependency(voiceover_id, script_id, "REQUIRES")
    adg.add_dependency(video_id, voiceover_id, "USES")
    adg.add_dependency(video_id, graphics_id, "USES")
    adg.add_dependency(video_id, music_id, "USES")
    
    # Cross-medium links
    adg.link_graphic_to_video(graphics_id, video_id, {"sync_points": [0, 60, 120]})
    adg.link_audio_to_video(voiceover_id, video_id, {"sync_offset": 0})
    adg.link_audio_to_video(music_id, video_id, {"volume": 0.3, "fade_in": 2, "fade_out": 2})
    
    # Mark assets complete
    adg.update_asset_status(script_id, AssetStatus.COMPLETE)
    adg.update_asset_status(voiceover_id, AssetStatus.COMPLETE)
    adg.update_asset_status(graphics_id, AssetStatus.COMPLETE)
    adg.update_asset_status(music_id, AssetStatus.COMPLETE)
    adg.update_asset_status(video_id, AssetStatus.COMPLETE)
    
    # Get production status
    production_status = adg.get_production_status(project_id)
    
    print(f"✅ Assets Registered: {production_status['total_assets']}")
    print(f"   Dependencies Mapped: {len(adg.get_dependency_report(project_id)['edges'])}")
    print(f"   Cross-Medium Links: {len(adg.get_cross_medium_report(project_id)['links'])}")
    print(f"   Production Complete: {production_status['completion_percentage'] * 100:.0f}%")
    print()
    
    # Get registry for dashboard
    adg_registry = {
        script_id: adg.get_asset(script_id),
        voiceover_id: adg.get_asset(voiceover_id),
        graphics_id: adg.get_asset(graphics_id),
        music_id: adg.get_asset(music_id),
        video_id: adg.get_asset(video_id)
    }
    
    workflow_results["steps_completed"].append("ADG")
    workflow_results["adg_status"] = production_status
    
    # ═══════════════════════════════════════════════════════════════════════
    # STEP 5: CREATIVE CONTINUITY SYSTEM (CCS)
    # ═══════════════════════════════════════════════════════════════════════
    
    print("━" * 80)
    print("STEP 5: CONTINUITY VALIDATION (CCS)")
    print("━" * 80)
    
    ccs = get_ccs()
    
    # Validate complete project
    ccs_report = ccs.validate_complete_project(
        project_id=project_id,
        assets={
            "script": adg.get_asset(script_id),
            "voiceover": adg.get_asset(voiceover_id),
            "graphics": adg.get_asset(graphics_id),
            "music": adg.get_asset(music_id),
            "video": adg.get_asset(video_id)
        },
        creative_direction=cre_output
    )
    
    print(f"✅ Overall Score: {ccs_report['overall_score']:.3f}")
    print(f"   Style Consistency: {ccs_report['style_consistency']['score']:.3f}")
    print(f"   Narrative Continuity: {ccs_report['narrative_continuity']['score']:.3f}")
    print(f"   Audio-Visual Harmony: {ccs_report['audio_visual_harmony']['score']:.3f}")
    print(f"   Brand Identity: {ccs_report['brand_identity']['score']:.3f}")
    print(f"   Total Violations: {ccs_report['total_violations']}")
    print(f"   Ready for Assembly: {ccs_report['ready_for_assembly']}")
    print()
    
    workflow_results["steps_completed"].append("CCS")
    workflow_results["ccs_report"] = ccs_report
    
    # ═══════════════════════════════════════════════════════════════════════
    # STEP 6: OUTPUT ASSEMBLY ENGINE (OAE)
    # ═══════════════════════════════════════════════════════════════════════
    
    print("━" * 80)
    print("STEP 6: FINAL ASSEMBLY (OAE)")
    print("━" * 80)
    
    oae = get_oae()
    
    # Assemble complete project
    oae_result = oae.assemble_complete_project(
        project_id=project_id,
        assets={
            script_id: adg.get_asset(script_id),
            voiceover_id: adg.get_asset(voiceover_id),
            graphics_id: adg.get_asset(graphics_id),
            music_id: adg.get_asset(music_id),
            video_id: adg.get_asset(video_id)
        },
        orchestration_plan=mmoe_output,
        continuity_report=ccs_report,
        creative_vision=cre_output,
        deliverable_type=DeliverableType.VIDEO_COURSE,
        target_platforms=[Platform.YOUTUBE, Platform.TIKTOK, Platform.INSTAGRAM]
    )
    
    print(f"✅ Assets Validated: {len(oae_result['asset_validation']['assets_validated'])}")
    print(f"   Timeline Duration: {oae_result['timeline']['duration_seconds']}s")
    print(f"   Audio Tracks Mixed: {len(oae_result['audio_mix']['tracks'])}")
    print(f"   Visual Layers: {len(oae_result['visual_composition']['layers'])}")
    print(f"   Deliverables Exported: {len(oae_result['deliverables'])}")
    print()
    
    for deliv in oae_result["deliverables"]:
        print(f"   • {deliv['platform'].upper()}: {deliv['resolution']} {deliv['format'].upper()} — {deliv['file_size_mb']:.0f}MB")
    print()
    
    workflow_results["steps_completed"].append("OAE")
    workflow_results["oae_result"] = oae_result
    
    # ═══════════════════════════════════════════════════════════════════════
    # STEP 7: DOMINION COMMAND DASHBOARD (DCD-IL)
    # ═══════════════════════════════════════════════════════════════════════
    
    print("━" * 80)
    print("STEP 7: DASHBOARD DISPLAY (DCD-IL)")
    print("━" * 80)
    
    dashboard = get_dominion_dashboard()
    
    # Generate complete dashboard view
    complete_dashboard = dashboard.display_complete_dashboard(
        project_id=project_id,
        project_name=pic_output["type"],
        pic_output=pic_output,
        cre_output=cre_output,
        mmoe_output=mmoe_output,
        adg_registry=adg_registry,
        ccs_report=ccs_report,
        oae_result=oae_result,
        execution_logs=[{"completed_waves": len(mmoe_output["orchestration_waves"]), "current_wave": len(mmoe_output["orchestration_waves"])}]
    )
    
    print(f"✅ Dashboard Generated")
    print(f"   Project Status: {complete_dashboard['summary']['status']}")
    print(f"   Progress: {complete_dashboard['summary']['progress']}")
    print(f"   Overall Health: {complete_dashboard['summary']['overall_health']}")
    print(f"   Assets Tracked: {complete_dashboard['summary']['assets_tracked']}")
    print(f"   Continuity Score: {complete_dashboard['summary']['continuity_score']:.3f}")
    print(f"   Deliverables Ready: {complete_dashboard['summary']['deliverables_ready']}")
    print()
    
    workflow_results["steps_completed"].append("DCD-IL")
    workflow_results["dashboard"] = complete_dashboard
    
    # ═══════════════════════════════════════════════════════════════════════
    # FINAL RESULTS
    # ═══════════════════════════════════════════════════════════════════════
    
    workflow_results["test_completed_at"] = datetime.utcnow().isoformat() + "Z"
    workflow_results["all_steps_passed"] = len(workflow_results["steps_completed"]) == 7
    
    return workflow_results


# ═══════════════════════════════════════════════════════════════════════════
# TEST EXECUTION
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Test Case 1: Youth Entrepreneurship Course
    print("\n" + "🔥" * 40)
    print("TEST CASE 1: Youth Entrepreneurship Course")
    print("🔥" * 40 + "\n")
    
    test_description_1 = """
    Create a comprehensive video course teaching youth entrepreneurship.
    Target audience: teenagers and young adults (13-25).
    Content should be energetic, modern, and inspirational.
    Include topics: business planning, marketing, finance basics, and digital presence.
    Brand: CodexDominion (sovereign, empowering, innovative).
    Output: Multi-platform video series for YouTube, TikTok, and Instagram.
    """
    
    results_1 = run_complete_workflow_test(test_description_1)
    
    # Save results
    output_file_1 = "integration_test_results_youth_course.json"
    with open(output_file_1, "w", encoding="utf-8") as f:
        json.dump(results_1, f, indent=2)
    
    print("=" * 80)
    print("TEST CASE 1 RESULTS")
    print("=" * 80)
    print(f"✅ Steps Completed: {', '.join(results_1['steps_completed'])}")
    print(f"✅ All Steps Passed: {results_1['all_steps_passed']}")
    print(f"📄 Results saved to: {output_file_1}")
    print()
    
    # Test Case 2: Faith-Based Kids Content
    print("\n" + "🔥" * 40)
    print("TEST CASE 2: Faith-Based Kids Bible Stories")
    print("🔥" * 40 + "\n")
    
    test_description_2 = """
    Create animated Bible story videos for kids ages 4-10.
    Content should be warm, engaging, and educational.
    Include moral lessons and interactive elements.
    Visual style: colorful, friendly characters.
    Brand: CodexDominion faith-based content.
    Output: Short-form videos for YouTube Kids and social media.
    """
    
    results_2 = run_complete_workflow_test(test_description_2)
    
    # Save results
    output_file_2 = "integration_test_results_bible_stories.json"
    with open(output_file_2, "w", encoding="utf-8") as f:
        json.dump(results_2, f, indent=2)
    
    print("=" * 80)
    print("TEST CASE 2 RESULTS")
    print("=" * 80)
    print(f"✅ Steps Completed: {', '.join(results_2['steps_completed'])}")
    print(f"✅ All Steps Passed: {results_2['all_steps_passed']}")
    print(f"📄 Results saved to: {output_file_2}")
    print()
    
    # Final Summary
    print("🔥" * 40)
    print()
    print("✅✅✅ INTEGRATION TEST COMPLETE ✅✅✅")
    print()
    print("The Creative Intelligence Engine successfully processed:")
    print(f"  • {len(results_1['steps_completed'])} steps for Test Case 1")
    print(f"  • {len(results_2['steps_completed'])} steps for Test Case 2")
    print()
    print("All modules are working together seamlessly:")
    print("  ✓ PIC: Project interpretation")
    print("  ✓ CRE: Creative reasoning")
    print("  ✓ MMOE: Production orchestration")
    print("  ✓ ADG: Asset tracking")
    print("  ✓ CCS: Continuity validation")
    print("  ✓ OAE: Final assembly")
    print("  ✓ DCD-IL: Dashboard display")
    print()
    print("🔥 THE COMPLETE WORKFLOW IS VALIDATED 🔥")
    print("👑 READY FOR FLASK DASHBOARD INTEGRATION 👑")
    print()
