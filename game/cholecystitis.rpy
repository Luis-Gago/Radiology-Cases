# Default store variables
default bodywall_images = 0
default chest_images = 0
default gallbladder_images = 0
default kidney_images = 0
default temp_image_input_bodywall = ""
default temp_image_input_chest = ""
default temp_image_input_gallbladder = ""
default temp_image_input_kidney = ""

# Gallbladder image selection state
default selected_gallbladder = False
default selected_fatstranding = False

init python:
    def validate_bodywall_input():
        txt = store.temp_image_input_bodywall.strip()
        if not txt:
            renpy.notify("Please enter a number.")
            return False
        try:
            num = int(txt)
        except ValueError:
            renpy.notify("Please enter a valid integer.")
            return False
        if 1 <= num <= 93:
            store.bodywall_images = num
            return True
        else:
            renpy.notify("Please enter a number between 1 and 93.")
            return False

    def validate_chest_input():
        txt = store.temp_image_input_chest.strip() if store.temp_image_input_chest else ""
        if not txt:
            renpy.notify("Please enter a number.")
            return False
        try:
            num = int(txt)
        except ValueError:
            renpy.notify("Please enter a valid integer.")
            return False
        if 94 <= num <= 253:
            store.chest_images = num
            return True
        else:
            renpy.notify("Please enter a number between 94 and 253.")
            return False

    def validate_gallbladder_input():
        txt = store.temp_image_input_gallbladder.strip() if store.temp_image_input_gallbladder else ""
        if not txt:
            renpy.notify("Please enter a number.")
            return False
        try:
            num = int(txt)
        except ValueError:
            renpy.notify("Please enter a valid integer.")
            return False
        if 1 <= num <= 93:
            store.gallbladder_images = num
            return True
        else:
            renpy.notify("Please enter a number between 1 and 93.")
            return False

    def validate_kidney_input():
        txt = store.temp_image_input_kidney.strip() if store.temp_image_input_kidney else ""
        if not txt:
            renpy.notify("Please enter a number.")
            return False
        try:
            num = int(txt)
        except ValueError:
            renpy.notify("Please enter a valid integer.")
            return False
        if 94 <= num <= 253:
            store.kidney_images = num
            return True
        else:
            renpy.notify("Please enter a number between 94 and 253.")
            return False

label cholecystitis:

    #Variables for hidden answers
    $ can_move_to_liver_chole = False
    $ can_move_to_gallbladder_chole = False
    $ can_move_to_pancreas_chole = False
    $ can_move_to_appy_chole = False
    $ can_move_to_chest_chole = False
    $ can_move_to_diagnosis_chole = False

    $ can_move_to_gallbladder_gallbladder_correct_menu = False
    $ can_move_to_gallbladder_fatstranding_correct_menu = False
    $ can_move_to_kidney_stone_menu = False
    $ can_move_to_kidney_nephrograms_menu = False

    scene bg readingroom
    a "You have selected Case Two."
    a "A patient has been brought into the ED and has been scanned with \"the tube of truth\" aka the CT scanner."
    a "You are being tasked with reading their CT abdomen pelvis with contrast."
    a "Use the EHR and PACS to fill out the report template I have provided."
    a "When you are ready, submit your report to continue to sign out."
    $ chole_score = 0  # Reset the score for this case

    # Initialize the EHR and PACS screens
    # Set the dynamic content for the EHR menu
    $ dynamic_content = "61-year-old F w/hx of GERD, diverticulosis, sarcoid p/w diffuse abdominal pain. Worse w/ movement but not eating. +nausea +vom"
    $ menu_visible = True
    $ menu_notification = True
    $ show_physical = True      # Show the Physical Exam button
    $ show_vitals = True   # Show the Vitals button 
    $ physical_text = "GI: Diffusely tender with guarding, +rebound, nondistended"
    $ vitals_text = "BP 119/55 Pulse 101 Temp 98.3°F(36.8°C) Resp 20"

    # Create a list of images for the DICOM viewer
    $ bone_images = [f"chole/Acute cholecystitis bone/ct_slice_{i:03d}.png" for i in range(1, 495)]
    $ soft_tissue_images = [f"chole/Acute cholecystitis soft tissue/ct_slice_{i:03d}.png" for i in range(1, 495)]
    $ lung_images = [f"chole/Acute cholecystitis lung/ct_slice_{i:03d}.png" for i in range(1, 495)]
    $ image_sets = [bone_images, soft_tissue_images, lung_images]
    $ set_names = ["Bone", "Soft Tx", "Lung"]

    # Initialize minimal caching for web deployment
    $ dicom_cache.aggressive_preload(image_sets[0], 0, 30)  
    $ dicom_cache.preload_all_sets(image_sets, 0) 

    show screen DICOMViewer(images=image_sets[0], image_sets=image_sets, current_set=0, set_names=set_names)
    
    # Show the Radiology Report screen
    call screen RadiologyReportCholecystitis()

    'You have submitted your report.'

    if player_answers_chole["liver"] == correct_answers_chole["liver"]:
        $ chole_score += 1
    if player_answers_chole["chest"] == correct_answers_chole["chest"]:
        $ chole_score += 1
    if player_answers_chole["kidney"] == correct_answers_chole["kidney"]:
        $ chole_score += 1
    if player_answers_chole["gallbladder"] == correct_answers_chole["gallbladder"]:
        $ chole_score += 1
    if player_answers_chole["bones"] == correct_answers_chole["bones"]:
        $ chole_score += 1
    if player_answers_chole["pancreas"] == correct_answers_chole["pancreas"]:
        $ chole_score += 1
    if player_answers_chole["bodywall"] == correct_answers_chole["bodywall"]:
        $ chole_score += 1
    if player_answers_chole["GI_tract"] == correct_answers_chole["GI_tract"]:
        $ chole_score += 1
    
    $ total_score = appy_score + chole_score + div_score

    $ menu_visible = False
    a "Let's review your report."

    jump bones_chole

# End of cholecystitis case
label end_cholecystitis:
    scene bg readingroom
    a "You have completed this case. Let's see how you did."
    a "You scored [chole_score] out of x."

    $ physical_text = ""
    $ vitals_text = ""
    $ show_physical = False
    $ show_vitals = False
    $ show_notification = False
    # $ appendicitis_var = False  # Disable this case for future runs

    jump start

label bones_chole:
    # Show the bones report section
    scene bg readingroom
    a "Let's start with the bones findings."
    a "You reported the Bones as: [player_answers_chole['bones']]"
    if player_answers_chole["bones"] == correct_answers_chole["bones"]:
        a "Great job, the bones are normal."
    else:
        a "Incorrect. The bones are normal, but you reported: [player_answers_chole['bones']]"
    jump bodywall_chole

label bodywall_chole:
    scene bg readingroom
    a "Now, let's look at the body wall findings."
    a "You reported the Body Wall as: [player_answers_chole['bodywall']]"
    if player_answers_chole["bodywall"] == correct_answers_chole["bodywall"]:
        a "Correct, there is a benign finding in the body wall."
    else:
        a "Incorrect. The body wall has a benign finding, but you reported: [player_answers_chole['bodywall']]"
    a "Can you see the benign finding in the body wall on the CT images?"
    a "Which images show the benign finding in the body wall?"
    
    jump bodywall_image_input
    
label bodywall_image_input:
    $ temp_image_input_bodywall = renpy.input("Enter a single axial image number (1–93) that shows the benign finding in the body wall:", length=2, allow="0123456789")
    $ temp_image_input_bodywall = temp_image_input_bodywall.strip()
    if not validate_bodywall_input():
        a "Invalid input. Please try again."
        jump bodywall_image_input
    jump bodywall_image_selection

label bodywall_image_selection:
    scene bg readingroom
    a "You selected image number [store.bodywall_images] for the benign finding in the body wall."
    if store.bodywall_images in [50, 51, 52]:
        a "Correct, the relevant axial images are 50, 51, or 52. Can you select the area on the axial image that shows the benign finding?"
        $ chole_score += 1
        $ total_score = appy_score + chole_score + div_score
        call screen bodywall_image_minigame
    else:
        a "Incorrect. The benign finding in the body wall is not in axial image number [store.bodywall_images]."
        a "The correct axial images are 50, 51, and 52."
        a "On the following image can you click on the area that shows the benign finding in the body wall?"
        $ chole_score -= 1
        $ total_score = appy_score + chole_score + div_score
        call screen bodywall_image_minigame

screen bodywall_image_minigame():
    default error_message = ""
    default screen_tooltip = ""
    zorder 100
    frame:
        xalign 0.9
        yalign 0.5
        xsize 550
        ysize 600

        add "chole/ct_umbilical_hernia.png"
        modal True

        imagebutton auto "chole/ct_umbilical_hernia_fat_%s.png":
            focus_mask True
            hovered SetScreenVariable("screen_tooltip", "Click to select.")
            unhovered SetScreenVariable("screen_tooltip", "")
            action Jump("correct_bodywall_image")

        imagebutton auto "chole/ct_umbilical_hernia_inc1_%s.png":
            focus_mask True
            hovered SetScreenVariable("screen_tooltip", "Click to select.")
            unhovered SetScreenVariable("screen_tooltip", "")
            action [
                SetScreenVariable("error_message", "Incorrect. Try again."),
                Function(lambda: setattr(store, "chole_score", chole_score - 1)),
                Function(lambda: setattr(store, "total_score", appy_score + chole_score + div_score)),
                Function(renpy.restart_interaction),
            ]

        imagebutton auto "chole/ct_umbilical_hernia_inc2_%s.png":
            focus_mask True
            hovered SetScreenVariable("screen_tooltip", "Click to select.")
            unhovered SetScreenVariable("screen_tooltip", "")
            action [
                SetScreenVariable("error_message", "Incorrect. Try again."),
                Function(lambda: setattr(store, "chole_score", chole_score - 1)),
                Function(lambda: setattr(store, "total_score", appy_score + chole_score + div_score)),
                Function(renpy.restart_interaction),
            ]

        if error_message:
            text "[error_message]" color "#f00" xalign 0.5 yalign 0.90
            timer 2.0 action SetScreenVariable("error_message", "") repeat False

        if screen_tooltip:
            text "[screen_tooltip]" color "#fff" xalign 0.5 yalign 0.98
        
label correct_bodywall_image:
    scene bg readingroom
    $ chole_score += 1
    $ total_score = appy_score + chole_score + div_score
    a "Great job! You selected the correct area showing the benign finding in the body wall"
    call screen fat_hernia_menu
    jump chest_chole

        
screen fat_hernia_menu():
    frame:
        xalign 1.0
        yalign 0.2
        xsize 700  # Set a fixed width for a more vertical look
        ypadding 40
        vbox:
            spacing 20  # Adds space between buttons
            text "What is the finding that you just selected?" xalign 0.5
            textbutton "Spigelian hernia" action Jump("fat_hernia_incorrect") xalign 0.5
            textbutton "Epigastric hernia" action Jump("fat_hernia_incorrect") xalign 0.5
            if can_move_to_chest_chole == False:
                textbutton "Umbilical hernia" action [SetVariable("chole_score", chole_score + 1), Jump("fat_hernia_correct")] xalign 0.5
            if can_move_to_chest_chole:
                textbutton "Move to Chest Report" action Jump("chest_chole") xalign 0.5 text_color "#FFD600"

label fat_hernia_correct:
    $ total_score = appy_score + chole_score + div_score
    $ can_move_to_chest_chole = True
    scene bg readingroom
    image chole umbilical hernia arrow = "chole/ct_umbilical_hernia_arrow@2.png"
    show chole umbilical hernia arrow at right_middle
    a "This fat containing umbilical hernia is a benign finding and does not require treatment or monitoring."
    hide chole umbilical hernia arrow

    call screen fat_hernia_menu

label fat_hernia_incorrect:
    scene bg readingroom
    a "Incorrect. This is not a finding in the bodywall."
    $ chole_score -= 1
    $ total_score = appy_score + chole_score + div_score

    call screen fat_hernia_menu


label chest_chole:
    scene bg readingroom
    a "Now, let's review the chest findings."
    a "You reported the Chest as: [player_answers_chole['chest']]"
    if player_answers_chole["chest"] == correct_answers_chole["chest"]:
        a "Correct, there is a benign finding in the chest."
        a "Can you identify for me which coronal images detail the benign chest finding?"
    else:
        a "Incorrect. The chest has a benign finding, but you reported: [player_answers_chole['chest']]"
        a "Can you identify for me which coronal images detail the benign chest finding?"
    
    jump chest_image_input

label chest_image_input:
    $ temp_image_input_chest = renpy.input("Enter a single image number (94-253) that shows the benign finding in the chest in the coronal images:", length=3, allow="0123456789")
    $ temp_image_input_chest = temp_image_input_chest.strip()
    if not validate_chest_input():
        a "Invalid input. Please try again."
        jump chest_image_input
    jump chest_image_selection
                    
label chest_image_selection:
    scene bg readingroom
    a "You selected image number [store.chest_images] for the benign finding in the body wall."
    if store.chest_images in range(155, 201):
        a "Correct, the finding is visible between images 155 and 200."
        a "What finding is visible in these images?"
        $ chole_score += 1
        $ total_score = appy_score + chole_score + div_score
        call screen chest_menu_chole
    else:
        a "Incorrect. The benign finding in the chest is not in coronal image number [store.chest_images]."
        a "The correct images are those between 155 and 200"
        a "What finding is visible in these images?"
        $ chole_score -= 1
        $ total_score = appy_score + chole_score + div_score
        call screen chest_menu_chole

screen chest_menu_chole:
    frame:
        xalign 1.0
        yalign 0.2
        xsize 700  # Set a fixed width for a more vertical look
        ypadding 40
        vbox:
            spacing 20  # Adds space between buttons
            text "Select the finding visible in the chest in image 155-200." xalign 0.5
            textbutton "0.2cm pulmonary nodule in the lower right lobe" action Jump("chest_incorrect_chole") xalign 0.5
            textbutton "Small left pneumothorax" action Jump("chest_incorrect_chole") xalign 0.5
            if can_move_to_liver_chole == False:
                textbutton "Subsegmental atelectasis in the lower lobes" action [SetVariable("chole_score", chole_score + 1), Jump("chest_atelectasis_chole")] xalign 0.5
            textbutton "Cardiomegaly" action Jump("chest_incorrect_chole") xalign 0.5
            if can_move_to_liver_chole:
                textbutton "Move to Liver Report" action Jump("liver_chole") xalign 0.5 text_color "#FFD600"

label chest_atelectasis_chole:
    $ total_score = appy_score + chole_score + div_score
    $ can_move_to_liver_chole = True
    image chole chest atelectasis = "chole/chole_atelectasis@2.png"  # Ensure the image is defined
    image chole chest example = "chole/chole_chest_example.jpg"  # Ensure the image is defined
    scene bg readingroom
    show chole chest atelectasis at right_middle
    a "Correct, there is subsegmental atelectasis in the lower lobes."
    a "Subsegmental atelectasis occurs when a small part of the lung is airless and collapsed."
    a "Subsegmental atelectasis can occur due to shallow breathing, cough suppression, compression of the lung, or a blocked airway."
    hide chole chest atelectasis
    show chole chest example at right_middle
    a "Here is an example of right middle lobe atelectasis on a CT scan."
    a "This image shows anterior displacement of the major fissure (arrow) and crowding of bronchi in the opacified segment of right middle lobe."
    hide chole chest example

    call screen chest_menu_chole

label chest_incorrect_chole:
    scene bg readingroom
    a "Incorrect. This is not a finding in the chest."
    $ chole_score -= 1
    $ total_score = appy_score + chole_score + div_score

    call screen chest_menu_chole

label liver_chole:
    $ total_score = appy_score + chole_score + div_score
    scene bg readingroom
    a "Now, let's review the liver findings."
    a "You reported the Liver as: [player_answers_chole['liver']]"
    if player_answers_chole["liver"] == correct_answers_chole["liver"]:
        a "Correct, the liver is normal."
    else:
        a "Incorrect. The liver is normal, but you reported: [player_answers_chole['liver']]"

    jump gallbladder_chole

label gallbladder_chole:
    scene bg readingroom
    a "Now, let's look at the gallbladder findings."
    a "You reported the Gallbladder as: [player_answers_chole['gallbladder']]"
    if player_answers_chole["gallbladder"] == correct_answers_chole["gallbladder"]:
        a "Correct, there is a pathological finding in the gallbladder."
        
    else:
        a "Incorrect. The gallbladder has a pathological finding, but you reported: [player_answers_chole['gallbladder']]"
    a "Enter an image number that shows the pathological finding in the gallbladder in the axial images."

    jump gallbladder_image_input

label gallbladder_image_input:
    $ temp_image_input_gallbladder = renpy.input("Enter a single image number (1-93) that shows the pathological finding in the gallbladder in the axial images:", length=2, allow="0123456789")
    $ temp_image_input_gallbladder = temp_image_input_gallbladder.strip()
    if not validate_gallbladder_input():
        a "Invalid input. Please try again."
        jump gallbladder_image_input
    jump gallbladder_image_selection

label gallbladder_image_selection:
    scene bg readingroom
    a "You selected image number [store.gallbladder_images] for the pathologic finding in the gallbladder."
    if store.gallbladder_images in range(30, 40):
        a "Correct, the finding is visible between images 30 and 40."
        a "Can you identify the pathology?"
        $ chole_score += 1
        $ total_score = appy_score + chole_score + div_score
        call screen gallbladder_image_minigame
    else:
        a "Incorrect. The pathologic finding in the chest is not in axial image number [store.gallbladder_images]."
        a "The correct images are those between 30 and 40"
        a "Can you identify the pathology?"
        $ chole_score -= 1
        $ total_score = appy_score + chole_score + div_score
        call screen gallbladder_image_minigame

screen gallbladder_image_minigame():
    default error_message = ""
    default screen_tooltip = ""
    zorder 100
    frame:
        xalign 0.9
        yalign 0.5
        xsize 550
        ysize 600

        add "chole/gallbladder.png"
        modal True

        # Gallbladder button
        if not selected_gallbladder:
            imagebutton auto "chole/gallbladder_gallbladder_%s.png":
                focus_mask True
                hovered SetScreenVariable("screen_tooltip", "Click to select.")
                unhovered SetScreenVariable("screen_tooltip", "")
                action [
                    SetScreenVariable("selected_gallbladder", True),
                    Jump("correct_gallbladder_gallbladder_image")
                ]

        # Fat stranding button
        if not selected_fatstranding:
            imagebutton auto "chole/gallbladder_fatstranding_%s.png":
                focus_mask True
                hovered SetScreenVariable("screen_tooltip", "Click to select.")
                unhovered SetScreenVariable("screen_tooltip", "")
                action [
                    SetScreenVariable("selected_fatstranding", True),
                    Jump("correct_gallbladder_fatstranding_image")
                ]

        # Incorrect buttons
        imagebutton auto "chole/gallbladder_liver_%s.png":
            focus_mask True
            hovered SetScreenVariable("screen_tooltip", "Click to select.")
            unhovered SetScreenVariable("screen_tooltip", "")
            action [
                SetScreenVariable("error_message", "Incorrect. Try again."),
                Function(lambda: setattr(store, "chole_score", chole_score - 1)),
                Function(lambda: setattr(store, "total_score", appy_score + chole_score + div_score)),
                Function(renpy.restart_interaction),
            ]

        imagebutton auto "chole/gallbladder_pancreas_%s.png":
            focus_mask True
            hovered SetScreenVariable("screen_tooltip", "Click to select.")
            unhovered SetScreenVariable("screen_tooltip", "")
            action [
                SetScreenVariable("error_message", "Incorrect. Try again."),
                Function(lambda: setattr(store, "chole_score", chole_score - 1)),
                Function(lambda: setattr(store, "total_score", appy_score + chole_score + div_score)),
                Function(renpy.restart_interaction),
            ]

        if error_message:
            text "[error_message]" color "#f00" xalign 0.5 yalign 0.90
            timer 2.0 action SetScreenVariable("error_message", "") repeat False

        if screen_tooltip:
            text "[screen_tooltip]" color "#fff" xalign 0.5 yalign 0.98

        # Show continue only after both correct have been selected
        if selected_gallbladder and selected_fatstranding:
            textbutton "Continue" action Jump("after_gallbladder_minigame") xalign 0.5 yalign 0.95

label correct_gallbladder_gallbladder_image:
    hide screen gallbladder_image_minigame
    scene bg readingroom
    $ chole_score += 1
    $ total_score = appy_score + chole_score + div_score
    $ selected_gallbladder = True
    a "Great job! Can you identify what you just selected?"
    call screen gallbladder_gallbladder_menu
    # Return to minigame for fatstranding
    if not selected_fatstranding:
        call screen gallbladder_image_minigame
    else:
        jump after_gallbladder_minigame

screen gallbladder_gallbladder_menu():
    frame:
        xalign 1.0
        yalign 0.2
        xsize 700  # Set a fixed width for a more vertical look
        ypadding 40
        vbox:
            spacing 20  # Adds space between buttons
            text "What is the finding that you just selected?" xalign 0.5
            textbutton "Gallstones causing obstruction of the common bile duct" action Jump("gallbladder_gallbladder_incorrect") xalign 0.5
            textbutton "A 2.5 cm gallbladder mass" action Jump("gallbladder_gallbladder_incorrect") xalign 0.5
            textbutton "Porcelain gallbladder" action Jump("gallbladder_gallbladder_incorrect") xalign 0.5
            if can_move_to_gallbladder_gallbladder_correct_menu == False:
                textbutton "Mild gallbladder distention and wall thickening" action [SetVariable("chole_score", chole_score + 1), Jump("gallbladder_gallbladder_correct_menu")] xalign 0.5
            if can_move_to_gallbladder_gallbladder_correct_menu:
                textbutton "Return" action [Hide("gallbladder_gallbladder_menu"), Show("gallbladder_image_minigame")] xalign 0.5 text_color "#FFD600"

label gallbladder_gallbladder_incorrect:
    scene bg readingroom    
    a "Incorrect. This is not a finding in the gallbladder."
    $ chole_score -= 1
    $ total_score = appy_score + chole_score + div_score
    call screen gallbladder_gallbladder_menu

label gallbladder_gallbladder_correct_menu:
    $ total_score = appy_score + chole_score + div_score
    $ can_move_to_gallbladder_gallbladder_correct_menu = True
    scene bg readingroom    
    image chole gallbladder distention transverse = "chole/gallbladder_distention_transverse_arrow@2.png"
    image chole gallbladder distention longitudinal = "chole/gallbladder_distention_longitudinal_arrow@2.png"
    show chole gallbladder distention transverse at right_middle
    a "Correct, the gallbladder is mildly distended."
    a "The gallbladder is mildly distended in this case, as it is larger than 4 cm in in a transverse measurement..."
    hide chole gallbladder distention transverse
    show chole gallbladder distention longitudinal at right_middle
    a "...and 9 cm in a longitudinal measurement."
    hide chole gallbladder distention longitudinal
    call screen gallbladder_gallbladder_menu

label correct_gallbladder_fatstranding_image:
    hide screen gallbladder_image_minigame
    scene bg readingroom
    $ chole_score += 1
    $ total_score = appy_score + chole_score + div_score
    $ selected_fatstranding = True
    a "Excellent! Can you identify what you just selected?"
    call screen gallbladder_fatstranding_menu
    # Return to minigame for gallbladder if not already selected
    if not selected_gallbladder:
        call screen gallbladder_image_minigame
    else:
        jump after_gallbladder_minigame

screen gallbladder_fatstranding_menu():
    frame:
        xalign 1.0
        yalign 0.2
        xsize 700  # Set a fixed width for a more vertical look
        ypadding 40
        vbox:
            spacing 20  # Adds space between buttons
            text "What is the finding that you just selected?" xalign 0.5
            textbutton "Biliary sludge" action Jump("gallbladder_fatstranding_incorrect") xalign 0.5
            textbutton "Inflammatory gallbladder polyps" action Jump("gallbladder_fatstranding_incorrect") xalign 0.5
            textbutton "Adenomyomatosis of the gallbladder" action Jump("gallbladder_fatstranding_incorrect") xalign 0.5
            if can_move_to_gallbladder_fatstranding_correct_menu == False:
                textbutton "Pericholecystic fluid and adjacent stranding" action [SetVariable("chole_score", chole_score + 1), Jump("gallbladder_fatstranding_correct_menu")] xalign 0.5
            if can_move_to_gallbladder_fatstranding_correct_menu:
                textbutton "Return" action [Hide("gallbladder_fatstranding_menu"), Show("gallbladder_image_minigame")] xalign 0.5 text_color "#FFD600"

label gallbladder_fatstranding_incorrect:
    scene bg readingroom
    a "Incorrect. This is not a finding in the gallbladder."
    $ chole_score -= 1
    $ total_score = appy_score + chole_score + div_score
    call screen gallbladder_fatstranding_menu

label gallbladder_fatstranding_correct_menu:
    $ total_score = appy_score + chole_score + div_score
    $ can_move_to_gallbladder_fatstranding_correct_menu = True
    scene bg readingroom
    image chole gallbladder fatstranding = "chole/gallbladder_fatstranding_arrow@2.png"
    show chole gallbladder fatstranding at right_middle
    a "Correct, there is fat stranding around the gallbladder."
    a "Fat stranding is a common finding in acute cholecystitis and indicates inflammation in the surrounding tissues."
    a "It is often seen as a haziness or increased density around the gallbladder on CT images."
    hide chole gallbladder fatstranding
    call screen gallbladder_fatstranding_menu

label after_gallbladder_minigame:
    hide screen gallbladder_image_minigame
    a "You have successfully identified both of the pathological findings in the gallbladder."
    # Continue your flow here
    jump pancreas_chole

label pancreas_chole:
    $ total_score = appy_score + chole_score + div_score
    scene bg readingroom
    a "Now, let's review the pancreas findings."
    a "You reported the Pancreas as: [player_answers_chole['pancreas']]"
    if player_answers_chole["pancreas"] == correct_answers_chole["pancreas"]:
        a "Correct, the pancreas is normal."
    else:
        a "Incorrect. The pancreas is normal, but you reported: [player_answers_chole['pancreas']]"

    jump kidneys_chole

label kidneys_chole:
    scene bg readingroom
    a "Now, let's review the kidney findings."
    a "You reported the Kidneys as: [player_answers_chole['kidney']]"
    if player_answers_chole["kidney"] == correct_answers_chole["kidney"]:
        a "Correct, the kidneys have benign findings."
    else:
        a "Incorrect. The kidneys have benign findings, but you reported: [player_answers_chole['kidney']]"
    call screen kidney_benign_menu

screen kidney_benign_menu():
    frame:
        xalign 1.0
        yalign 0.2
        xsize 700  # Set a fixed width for a more vertical look
        ypadding 40
        vbox:
            spacing 20  # Adds space between buttons
            text "What are the two benign findings in the kidney?" xalign 0.5
            textbutton "Bilateral hydronephrosis" action Jump("kidney_benign_incorrect") xalign 0.5
            if can_move_to_kidney_stone_menu == False:
                textbutton "Punctate calcification" action [SetVariable("chole_score", chole_score + 1), Jump("kidney_image_input_stone")] xalign 0.5
            textbutton "Calyceal Diverticula" action Jump("kidney_benign_incorrect") xalign 0.5
            textbutton "Simple Renal Cyst" action Jump("kidney_benign_incorrect") xalign 0.5
            if can_move_to_kidney_nephrograms_menu == False:
                textbutton "Bilateral symmetric nephrograms" action [SetVariable("chole_score", chole_score + 1), Jump("kidney_image_input_nephrograms")] xalign 0.5
            if can_move_to_kidney_nephrograms_menu and can_move_to_kidney_stone_menu:
                textbutton "Continue" action Jump("GI_Chole") xalign 0.5 text_color "#FFD600"

label kidney_benign_incorrect:
    scene bg readingroom
    a "Incorrect. This is not a finding in the kidney."
    $ chole_score -= 1
    $ total_score = appy_score + chole_score + div_score

    call screen kidney_benign_menu

label kidney_image_input_stone:
    $ can_move_to_kidney_stone_menu = True
    a "Correct, there is a punctate calcification visible on the CT scan."
    $ temp_image_input_kidney = renpy.input("Enter a single coronal image number (94-253) that shows the punctate calcification:", length=3, allow="0123456789")
    $ temp_image_input_kidney = temp_image_input_kidney.strip()
    if not validate_kidney_input():
        a "Invalid input. Please try again."
        jump kidney_image_input_stone
    jump kidney_image_selection_stone

label kidney_image_selection_stone:
    scene bg readingroom
    a "You selected image number [store.kidney_images] for the punctate calcification."
    if store.kidney_images in range(187, 189):
        a "Correct, the punctate calcification is visible in images 187 and 188."
        $ chole_score += 1
        $ total_score = appy_score + chole_score + div_score
    else:
        a "Incorrect. punctate calcification is not in axial image number [store.kidney_images]."
        a "The correct images are 187 and 188"
        $ chole_score -= 1
        $ total_score = appy_score + chole_score + div_score
    image kidney stone = "chole/kidneystone_chole@2.png"
    show kidney stone at right_middle
    a "There is a punctate calcification in the left lower pole, which most likely represents a nonobstructing renal stone."
    hide kidney stone
    call screen kidney_benign_menu

label kidney_image_input_nephrograms:
    $ can_move_to_kidney_nephrograms_menu = True
    a "Correct, there are bilateral symmetric nephrograms visible on the CT scan."
    $ temp_image_input_kidney = renpy.input("Enter a single coronal image number (94-253) that shows the nephrograms:", length=3, allow="0123456789")
    $ temp_image_input_kidney = temp_image_input_kidney.strip()
    if not validate_kidney_input():
        a "Invalid input. Please try again."
        jump kidney_image_input_nephrograms
    jump kidney_image_selection_nephrograms

label kidney_image_selection_nephrograms:
    scene bg readingroom
    a "You selected image number [store.kidney_images] for the nephrograms."
    if store.kidney_images in range(183, 188):
        a "Correct, the nephrograms are visible between images 183 and 187."
        $ chole_score += 1
        $ total_score = appy_score + chole_score + div_score
    else:
        a "Incorrect. nephrograms are not in axial image number [store.kidney_images]."
        a "The correct images are between 183 and 187"
        $ chole_score -= 1
        $ total_score = appy_score + chole_score + div_score
    image bilateral symmetric nephrograms = "chole/bilateral_symmetric_nephrograms@2.png"
    show bilateral symmetric nephrograms at right_middle
    a "There are bilateral symmetric nephrograms without hydronephrosis."
    a "This finding occurs when intravenous contrast media is retained by both kidneys for more than 3 minutes."
    a "Causes include systemic hypotension, bilateral intrarenal obstruction, bilateral renal artery/vein stenosis, or bilateral obstructive uropathy among others."
    hide bilateral symmetric nephrograms
    call screen kidney_benign_menu

label GI_Chole:
    scene bg readingroom
    a "Now, let's review the GI tract findings."
    a "You reported the GI tract as: [player_answers_chole['GI_tract']]"
    if player_answers_chole["GI_tract"] == correct_answers_chole["GI_tract"]:
        a "Correct, the GI tract has benign findings."
    else:
        a "Incorrect. The GI tract has benign findings, but you reported: [player_answers_chole['GI_tract']]"
    call screen GI_tract_benign_menu
