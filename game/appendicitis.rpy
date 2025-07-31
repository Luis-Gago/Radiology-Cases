label appendicitis:

    scene bg readingroom
    a "You have selected Case One."
    a "A patient has been brought into the ED and has been scanned with \"the tube of truth\" aka the CT scanner."
    a "You are being tasked with reading their CT abdomen pelvis with contrast."
    a "Use the EHR and PACS to fill out the report template I have provided."
    a "When you are ready, submit your report to continue to sign out."
    $ appy_score = 0  # Reset the score for this case
    
    #Variables for hidden answers
    $ can_move_to_liver = False
    $ can_move_to_gallbladder = False
    $ can_move_to_gallbladder_1 = False
    $ can_move_to_appy = False
    $ can_move_to_diagnosis = False

    scene bg readingroom

    # Set the dynamic content for the EHR menu
    $ dynamic_content = "25yo m w/ hx of gerd presents with sharp r.sided abd pain radiating to epigastic and sub xyphoid regions. (+)anorexia, (+)watery diarrhea, (+)emesis."
    $ menu_visible = True
    $ menu_notification = True
    $ show_physical = True      # Show the Physical Exam button
    $ show_vitals = True   # Show the Vitals button 
    $ physical_text = "Soft, ND, (-)rovsigns, (+)mcburney's, (-)cva tenderness, (-)masses, (-)RUQ/epigastric tenderness."
    $ vitals_text = "BP: 136/75, HR: 60, Temp: 98°F (36.7°C)"

    # Create a list of images for the DICOM viewer
    $ bone_images = [f"appy/Acute appendicitis bone/ct_slice_{i:03d}.png" for i in range(1, 366)]
    $ soft_tissue_images = [f"appy/Acute appendicitis soft tissue/ct_slice_{i:03d}.png" for i in range(1, 366)]
    $ lung_images = [f"appy/Acute appendicitis lung/ct_slice_{i:03d}.png" for i in range(1, 366)]
    $ image_sets = [bone_images, soft_tissue_images, lung_images]
    $ set_names = ["Bone", "Soft Tx", "Lung"]
    
    # Initialize minimal caching for web deployment
    $ dicom_cache.aggressive_preload(image_sets[0], 0, 30)  
    $ dicom_cache.preload_all_sets(image_sets, 0) 
    
    show screen DICOMViewer(images=image_sets[0], image_sets=image_sets, current_set=0, set_names=set_names)
    
    # Show the Radiology Report screen
    call screen RadiologyReportAppendicitis()

    'You have submitted your report.'

    if player_answers_appy["liver"] == correct_answers_appy["liver"]:
        $ appy_score += 1
    if player_answers_appy["chest"] == correct_answers_appy["chest"]:
        $ appy_score += 1
    if player_answers_appy["appendix"] == correct_answers_appy["appendix"]:
        $ appy_score += 1
    if player_answers_appy["kidney"] == correct_answers_appy["kidney"]:
        $ appy_score += 1
    if player_answers_appy["gallbladder"] == correct_answers_appy["gallbladder"]:
        $ appy_score += 1
    if player_answers_appy["bones"] == correct_answers_appy["bones"]:
        $ appy_score += 1
    
    $ total_score = appy_score + chole_score + div_score

    $ menu_visible = False
    a "Let's review your report."
    
    jump bones_appy

# End of appendicitis case
label end_appendicitis:
    scene bg readingroom
    a "You have completed this case. Let's see how you did."
    a "You scored [appy_score] out of 13."

    $ physical_text = ""
    $ vitals_text = ""
    $ show_physical = False
    $ show_vitals = False
    $ show_notification = False
    # $ appendicitis_var = False  # Disable this case for future runs

    jump start

label bones_appy:
    # Show the bones report section
    scene bg readingroom
    a "Let's start with the bones findings."
    a "You reported the Bones as: [player_answers_appy['bones']]"
    if player_answers_appy["bones"] == correct_answers_appy["bones"]:
        a "Great job, the bones are normal."
    else:
        a "Incorrect. The bones are normal, but you reported: [player_answers_appy['bones']]"
    a "Let's move onto the chest findings."
    jump chest_appy

# Chest Report Section
label chest_appy:
    # Move to the chest section of the report
    scene bg readingroom
    a "Let me see..."
    a "You reported the Chest as: [player_answers_appy['chest']]"
    if player_answers_appy["chest"] == correct_answers_appy["chest"]:
        a "Great job, the chest has a benign finding."
    else:
        a "Incorrect. The chest has a benign finding, but you reported: [player_answers_appy['chest']]"
    a "Can you see the benign findings in the chest image?" 
    call screen chest_menu

screen chest_menu:
    frame:
        xalign 1.0
        yalign 0.2
        xsize 700  # Set a fixed width for a more vertical look
        ypadding 40
        vbox:
            spacing 20  # Adds space between buttons
            text "Select the findings in the chest image." xalign 0.5
            textbutton "0.5cm pulmonary nodule in the lower right lobe" action Jump("chest_incorrect") xalign 0.5
            textbutton "Small left pneumothorax" action Jump("chest_incorrect") xalign 0.5
            if can_move_to_liver == False:
                textbutton "0.3 cm juxtapleural nodule in the left lower lobe" action [SetVariable("appy_score", appy_score + 1), Jump("chest_nodule")] xalign 0.5
            if can_move_to_liver:
                textbutton "Move to Liver Report" action Jump("liver_appy") xalign 0.5 text_color "#FFD600"

label chest_nodule:
    $ total_score = appy_score + chole_score + div_score
    $ can_move_to_liver = True
    image appy nodule = "appy/appy_nodule@1.5.png"  # Ensure the image is defined
    image appy chest example = "appy/appy_chest_example@0.5.jpg"  # Ensure the image is defined
    scene bg readingroom
    show appy nodule at right_middle
    a "Correct, the 0.3 cm juxtapleural nodule in the left lower lobe is a benign finding."
    a "This nodule can also be described as pleura-based: in contact with the pleura but not derived from the pleura"
    a "This is likely a lymph node and is of doubtful significance in a patient of this age."
    a "Note that intrapulmonary lymph nodes are characteristically homogeneous, well-defined, smooth, ovoid, small (usually <12 cm), and located inferior to the carina."
    a "Hold on I have another example somewhere..."
    hide appy nodule
    show appy chest example at right_middle
    a "If peripheral nodules have all the typical features of intraparenchymal lymph nodes they are likely to be benign and follow-up at 1 year may be appropriate"
    hide appy chest example

    call screen chest_menu

label chest_incorrect:
    scene bg readingroom
    a "Incorrect. This is not a finding in the chest."
    $ appy_score -= 1
    $ total_score = appy_score + chole_score + div_score

    call screen chest_menu


# Liver Report Section
label liver_appy:
    scene bg readingroom
    a "Let's move onto the liver findings."
    a "You reported the Liver as: [player_answers_appy['liver']]"
    if player_answers_appy["liver"] == correct_answers_appy["liver"]:
        a "Good eye, the liver has benign findings."
    else:
        a "Incorrect. The liver has benign findings, but you reported: [player_answers_appy['liver']]"
    a "Can you see the benign findings in the liver image?"

    call screen liver_menu

screen liver_menu():
    frame:
        xalign 1.0
        yalign 0.2
        xsize 700  # Set a fixed width for a more vertical look
        ypadding 40
        vbox:
            spacing 20  # Adds space between buttons
            text "Select the benign findings in the liver image." xalign 0.5
            if can_move_to_gallbladder_1 == False:
                textbutton "Inferior extension of the right hepatic lobe (Riedel's configuration)." action [SetVariable("appy_score", appy_score + 1), Jump("Riedels_configuration")] xalign 0.5
            textbutton "Hemangioma in the left lobe of the liver." action Jump("liver_incorrect") xalign 0.5
            textbutton "Adenoma in the right lobe of the liver." action Jump("liver_incorrect") xalign 0.5
            if can_move_to_gallbladder == False:
                textbutton "Hypodensities in the liver too small to characterize." action [SetVariable("appy_score", appy_score + 1), Jump("hypodensities")] xalign 0.5
            if can_move_to_gallbladder and can_move_to_gallbladder_1:
                textbutton "Move to Gallbladder/Pancreas Report" action Jump("gallbladder_appy") xalign 0.5 text_color "#FFD600"

label Riedels_configuration:
    $ total_score = appy_score + chole_score + div_score
    $ can_move_to_gallbladder_1 = True
    image appy riedel = "appy/appy_riedel.png"  # Ensure the image is defined
    image appy riedel example = "appy/appy_riedel_example@0.8.png"  # Ensure the image is defined
    scene bg readingroom
    show appy riedel at right_middle
    a "Correct, Riedel's lobe is a normal anatomical variant of the liver."
    a "Riedel lobe is a tongue-like, inferior projection of the right lobe of the liver beyond the level of the most inferior costal cartilage on cross-sectional images."
    a "This finding is benign anatomical variant and does not require any intervention."
    a "It is important to be able to differentiate Riedel's lobe from pathological conditions such as hepatomegaly or masses."
    hide appy riedel
    show appy riedel example at right_middle
    a "Here is another example of Riedel's lobe."
    hide appy riedel example
    call screen liver_menu

label hypodensities:
    $ total_score = appy_score + chole_score + div_score
    $ can_move_to_gallbladder = True
    image appy liver hypodensity = "appy/appy_liver_hypodensity.png"  # Ensure the image is defined
    scene bg readingroom
    show appy liver hypodensity at right_middle
    a "Correct, these hypodensities in the liver are too small to characterize."
    a "Because the prevalence of benign focal liver lesions in adults is high, with at least one lesion seen in up to 15 percent of patients..."
    a "...accurate characterization of incidentally detected lesions is an important objective of diagnostic imaging."
    a "These findings are often benign and do not require immediate action."
    a "However, they should be monitored over time."
    hide appy liver hypodensity

    call screen liver_menu

label liver_incorrect:
    scene bg readingroom
    a "Incorrect. This is not a benign finding in the liver."
    $ appy_score -= 1
    $ total_score = appy_score + chole_score + div_score

    call screen liver_menu


label gallbladder_appy:
    # Move to the gallbladder section of the report
    image appy gallbladder = "appy/appy_gallbladder.png" 
    scene bg readingroom
    a "Now, let's review the gallbladder and pancreas findings."
    a "You reported the Gallbladder and Pancreas as: [player_answers_appy['gallbladder']]"
    show appy gallbladder at right_middle
    if player_answers_appy["gallbladder"] == correct_answers_appy["gallbladder"]:
        a "Well done, the gallbladder is present and has no biliary ductal dilatation."
        a "The pancreas is normal in size and enhances homogenously."
    else:
        a "Incorrect. The gallbladder and pancreas are normal, but you reported: [player_answers_appy['gallbladder']]"
        a "The gall bladder is present and has no biliary ductal dilatation."
        a "The pancreas is normal in size and enhances homogenously."
    hide appy gallbladder
    jump kidney_appy


label kidney_appy:
    # Move to the kidney section of the report
    scene bg readingroom
    a "Onwards, let's review the kidney findings."
    a "You reported the Kidneys as: [player_answers_appy['kidney']]"
    if player_answers_appy["kidney"] == correct_answers_appy["kidney"]:
        a "Excellent, the kidneys have a pathological process."
    else:
        a "Incorrect. The kidneys appear to be undergoing a pathological process, but you reported: [player_answers_appy['kidney']]"
    a "Can you see the pathological process in the kidney image?"

    call screen kidney_menu

screen kidney_menu():
    frame:
        xalign 1.0
        yalign 0.2
        xsize 700  # Set a fixed width for a more vertical look
        ypadding 40
        vbox:
            spacing 20  # Adds space between buttons
            text "Select the pathological process in the kidney image." xalign 0.5
            if can_move_to_appy == False:
                textbutton "Distal right ureteral thickening." action [SetVariable("appy_score", appy_score + 1), Jump("renal_thickening")] xalign 0.5
            textbutton "Renal stone in the right ureter." action Jump("kidney_incorrect") xalign 0.5
            textbutton "Renal mass in the right kidney." action Jump("kidney_incorrect") xalign 0.5
            if can_move_to_appy:
                textbutton "Move to Appendix Report" action Jump("appendix_appy") xalign 0.5 text_color "#FFD600"

label kidney_incorrect:
    scene bg readingroom
    a "Incorrect. This is not a pathological process in the kidney."
    $ appy_score -= 1
    $ total_score = appy_score + chole_score + div_score

    call screen kidney_menu

label renal_thickening:
    $ total_score = appy_score + chole_score + div_score
    $ can_move_to_appy = True
    image appy ureter = "appy/appy_ureter.png" 
    scene bg readingroom
    show appy ureter at right_middle
    a "Correct, distal right ureteral thickening is present."
    a " Mild distal right ureteral thickening is likely reactive to an inflammatory process."
    hide appy ureter
    call screen kidney_menu

label appendix_appy:
    # Move to the appendix section of the report
    scene bg readingroom
    a "Finally, let's review the appendix findings."
    a "You reported the Appendix as: [player_answers_appy['appendix']]"
    if player_answers_appy["appendix"] == correct_answers_appy["appendix"]:
        a "Great job, the appendix has pathological findings."
    else:
        a "Incorrect. The appendix has pathological findings, but you reported: [player_answers_appy['appendix']]"
    a "Can you see the pathological findings in the appendix image?"    
    call screen appendix_menu

screen appendix_menu():
    frame:
        xalign 1.0
        yalign 0.2
        xsize 700  # Set a fixed width for a more vertical look
        ypadding 40
        vbox:
            spacing 20  # Adds space between buttons
            text "Select the pathological findings in the appendix image." xalign 0.5
            textbutton "Appendicolith in the appendix." action [Jump("appendix_incorrect")] xalign 0.5
            if can_move_to_diagnosis == False:
                textbutton "Dialated appendix with wall thickening." action [SetVariable("appy_score", appy_score + 1), Jump("appendicitis_with_fluid")] xalign 0.5
            textbutton "Ruptured appendix with drainable fluid collection." action Jump("appendix_incorrect") xalign 0.5
            if can_move_to_diagnosis:
                textbutton "Move to Diagnosis" action Jump("appy_diagnosis") xalign 0.5 text_color "#FFD600"

label appendix_incorrect:
    scene bg readingroom
    a "Incorrect. This is not the pathological finding in the appendix."
    $ appy_score -= 1    
    $ total_score = appy_score + chole_score + div_score
    call screen appendix_menu

label appendicitis_with_fluid:
    $ total_score = appy_score + chole_score + div_score
    $ can_move_to_diagnosis = True
    image appy = "appy/appy@2.png"
    scene bg readingroom
    show appy at right_middle
    a "Correct, the appendix is dilated and fluid-filled measuring 1.0 cm in diameter."
    a "There is wall thickening and hyperenhancement throughout the appendix with periappendiceal fat stranding and free fluid."
    a "No appendicolith or drainable fluid collection is identified.  The diameter at the base measures 1.0 cm."
    hide appy
    image appy example = "appy/appy_example@0.8.jpeg"
    show appy example at right_middle
    a "Here is another good example of a dilated appendix with wall thickening and hyperenhancement."
    a "Dilated appendix with a maximum diameter of 12 mm showing a fluid-filled lumen and thick enhanced walls. Minimal reactionary pelvic free fluid."
    hide appy example
    call screen appendix_menu


# Diagnosis Section
label appy_diagnosis:

    hide screen DICOMViewer

    scene bg readingroom
    a "Now, let's summarize your findings."
    a "What do you think the diagnosis is?"
    menu:
        "Acute appendicitis":
            a "Correct, the diagnosis is acute appendicitis."
            a "The key findings include a dilated appendix with wall thickening and hyperenhancement, periappendiceal fat stranding, and free fluid."
            $ appy_score += 1
            $ total_score = appy_score + chole_score + div_score

        "Cholecystitis":
            a "Incorrect, this is not the diagnosis for this case."
            a "The correct answer is acute appendicitis. The key findings include a dilated appendix with wall thickening and hyperenhancement, periappendiceal fat stranding, and free fluid."
            $ appy_score -= 1
            $ total_score = appy_score + chole_score + div_score
         
        "Diverticulitis":
            a "Incorrect, this is not the diagnosis for this case."
            a "The correct answer is acute appendicitis. The key findings include a dilated appendix with wall thickening and hyperenhancement, periappendiceal fat stranding, and free fluid."
            $ appy_score -= 1
            $ total_score = appy_score + chole_score + div_score
        
        "Pancreatitis":
            a "Incorrect, this is not the diagnosis for this case."
            a "The correct answer is acute appendicitis. The key findings include a dilated appendix with wall thickening and hyperenhancement, periappendiceal fat stranding, and free fluid."
            $ appy_score -= 1
            $ total_score = appy_score + chole_score + div_score
    
    a "Note some other key findings from the case:"
    a "Rebound tenderness over the appendix (e.g. McBurney sign)."
    a "Diarrhea, anorexia, and emesis."
    a "And note that eventually their white count came back elevated..."
    image alvarado = "appy/alvarado_score.png"
    show alvarado at top
    a "...giving them an Alvarado score of 9 out of 10 which is definite appendicitis."
    hide alvarado

    a "How do you think the patient should be managed?"
    menu:
        "Immediate surgical intervention":
            a "Correct, surgical intervention is the appropriate management for acute appendicitis."
            $ appy_score += 1
            $ total_score = appy_score + chole_score + div_score
        "Medical management":
            a "Incorrect, while possible this is a non-standard approach for acute appendicitis."
            a "The standard management is surgical intervention."
            $ appy_score -= 1
            $ total_score = appy_score + chole_score + div_score
        "Observation":
            a "Incorrect, observation is not appropriate for acute appendicitis."
            a "The standard management is surgical intervention."
            $ appy_score -= 1
            $ total_score = appy_score + chole_score + div_score
    
    a "Would you like to restart the case or return to the main menu?"
    menu:
        "Restart Case":
            jump appendicitis

        "Return to Main Menu":
            jump end_appendicitis





   
    
    


