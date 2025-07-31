label diverticulitis:

    scene bg readingroom
    a "You have selected Case Three."
    a "A patient has been brought into the ED and has been scanned with \"the tube of truth\" aka the CT scanner."
    a "You are being tasked with reading their CT abdomen pelvis with contrast."
    a "Use the EHR and PACS to fill out the report template I have provided."
    a "When you are ready, submit your report to continue to sign out."
    $ chole_score = 0  # Reset the score for this case

    scene bg readingroom
    
    # Set the dynamic content for the EHR menu
    $ dynamic_content = ""
    $ menu_visible = True
    $ menu_notification = True
    $ show_physical = True      # Show the Physical Exam button
    $ show_vitals = True   # Show the Vitals button 
    $ physical_text = ""
    $ vitals_text = ""

    # Create a list of images for the DICOM viewer
    $ bone_images = [f"divertic/Acute diverticulitis bone/ct_slice_{i:03d}.png" for i in range(1, 547)]
    $ soft_tissue_images = [f"divertic/Acute diverticulitis soft tissue/ct_slice_{i:03d}.png" for i in range(1, 547)]
    $ lung_images = [f"divertic/Acute diverticulitis lung/ct_slice_{i:03d}.png" for i in range(1, 547)]
    $ image_sets = [bone_images, soft_tissue_images, lung_images]
    $ set_names = ["Bone", "Soft Tx", "Lung"]
    show screen DICOMViewer(images=image_sets[0], image_sets=image_sets, current_set=0, set_names=set_names)
    
    # Show the Radiology Report screen
    call screen RadiologyReportDiverticulitis()