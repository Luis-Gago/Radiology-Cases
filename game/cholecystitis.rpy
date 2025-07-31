# Default store variables
default bodywall_images = 0
default chest_images = 0
default temp_image_input = ""


# Python functions for this script
python:
    def restart_with_score_update(score_var, score_change, total_var, total_calc):
        renpy.store[score_var] += score_change
        renpy.store[total_var] = total_calc
        renpy.restart_interaction()

label cholecystitis:

    #Variables for hidden answers
    $ can_move_to_liver_chole = False
    $ can_move_to_gallbladder_chole = False
    $ can_move_to_pancreas_chole = False
    $ can_move_to_appy_chole = False
    $ can_move_to_chest_chole = False
    $ can_move_to_diagnosis_chole = False

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

    call screen bodywall_image_input

    jump bodywall_image_selection

screen bodywall_image_input():
    frame:
        xalign 0.9
        yalign 0.5
        xsize 600
        ysize 300
        
        vbox:
            spacing 20
            xalign 0.5
            yalign 0.5
            
            text "Enter a single image number (1-93) that shows the benign finding in the body wall in the axial images:" xalign 0.5
            
            input:
                value VariableInputValue("temp_image_input")
                length 2
                allow "0123456789"
                xalign 0.5
                
            hbox:
                spacing 20
                xalign 0.5
                
                textbutton "Submit":
                    action [Function(validate_bodywall_input), Return()]
                    
                textbutton "Cancel":
                    action Return()

init python:
    def validate_bodywall_input():
        try:
            num = int(store.temp_image_input.strip())
            if 1 <= num <= 93:
                store.bodywall_images = num
                return True  # Return True if valid
            else:
                renpy.notify("Please enter a number between 1 and 93.")
                return False  # Return False if invalid
        except (ValueError, AttributeError):
            renpy.notify("Please enter a valid number.")
            return False

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
    $ appy_score -= 1
    $ total_score = appy_score + chole_score + div_score

    call screen fat_hernia_menu


label chest_chole:
    scene bg readingroom
    a "Now, let's review the chest findings."
    a "You reported the Chest as: [player_answers_chole['chest']]"
    if player_answers_chole["chest"] == correct_answers_chole["chest"]:
        a "Correct, there is a benign finding in the chest."
    else:
        a "Incorrect. The chest has a benign finding, but you reported: [player_answers_chole['chest']]"
        a "Can you identify for me which axial images detail the benign chest finding?"

screen chest_image_input():
    frame:
        xalign 0.9
        yalign 0.5
        xsize 600
        ysize 300
        
        vbox:
            spacing 20
            xalign 0.5
            yalign 0.5
            
            text "Enter a single image number (1-) that shows the benign finding in the chest in the axial images:" xalign 0.5
            
            input:
                value VariableInputValue("temp_image_input")
                length 2
                allow "0123456789"
                xalign 0.5
                
            hbox:
                spacing 20
                xalign 0.5
                
                textbutton "Submit":
                    action [Function(validate_chest_input), Return()]
                    
                textbutton "Cancel":
                    action Return()

init python:
    def validate_chest_input():
        try:
            num = int(store.temp_image_input.strip())
            if 1 <= num <= 93:
                store.chest_images = num
                return True  # Return True if valid
            else:
                renpy.notify("Please enter a number between 1 and 93.")
                return False  # Return False if invalid
        except (ValueError, AttributeError):
            renpy.notify("Please enter a valid number.")
            return False

label chest_image_selection:
    scene bg readingroom
    a "You selected image number [store.chest_images] for the benign finding in the body wall."
    if store.chest_images in [50, 51, 52]:
        a "Correct, the relevant axial images are , , or . Can you select the area on the axial image that shows the benign finding?"
        $ chole_score += 1
        $ total_score = appy_score + chole_score + div_score
        call screen chest_image_minigame
    else:
        a "Incorrect. The benign finding in the chest is not in axial image number [store.chest_images]."
        a "The correct axial images are , , and ."
        a "On the following image can you click on the area that shows the benign finding in the chest?"
        $ chole_score -= 1
        $ total_score = appy_score + chole_score + div_score
        call screen chest_image_minigame

screen chest_image_minigame():
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
        
label correct_chest_image:
    scene bg readingroom
    $ chole_score += 1
    $ total_score = appy_score + chole_score + div_score
    a "Great job! You selected the correct area showing the benign finding in the chest"
    call screen fat_hernia_menu
    jump chest_chole