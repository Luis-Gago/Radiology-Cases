label breast_case_1:
    # Image selection minigame variable
    $ selected_calcs = False
    scene bg readingroom
    h "Welcome to the Breast Imaging Case."
    h "Use the EHR and PACS to fill out the report template I have provided."
    h "When you are ready, submit your report to continue to sign out."
    
    # Reset breast score for this case:
    $ breast_score = 0
    $ total_score = breast_score + chole_score + div_score + appy_score

    # Set the dynamic content for the EHR menu
    $ dynamic_content = "37 year old female returning after abnormal screening mammogram"
    $ menu_visible = True
    $ menu_notification = True
    $ show_physical = True      # Show the Physical Exam button
    $ show_history = True        # Show the History button
    $ physical_text = "Palpable abnormality in her left breast"
    $ history_text = "FMH includes breast cancer in paternal aunt"

    # Create a list of images for the DICOM viewer
    $ r_mllm_images = [f"breast/R-MLLM/R-MLLM_{i:01d}.png" for i in range(1, 4)]
    $ l_mllm_images = [f"breast/L-MLLM/L-MLLM_{i:01d}.png" for i in range(1, 4)]
    $ r_tomo_images = [f"breast/TomoR/Tomo_R_{i:01d}.png" for i in range(1, 46)]
    $ l_tomo_images = [f"breast/TomoL/Tomo_L_{i:01d}.png" for i in range(1, 69)]
    $ original_mammo_images = [f"breast/OM/OM_{i:01d}.png" for i in range(1, 5)]
    $ image_sets = [original_mammo_images, l_mllm_images, r_mllm_images, l_tomo_images, r_tomo_images]
    $ set_names = ["Screening", "L-ML/LM", "R-ML/LM", "L-Tomo", "R-Tomo"]

    # Initialize minimal caching for web deployment
    $ dicom_cache.aggressive_preload(image_sets[0], 0, 30)  
    $ dicom_cache.preload_all_sets(image_sets, 0) 

    show screen DICOMViewer(images=image_sets[0], image_sets=image_sets, current_set=0, set_names=set_names)

    # Show the Radiology Report screen
    call screen RadiologyReportBreast()

    'You have submitted your report.'

    if player_answers_breast["density"] == correct_answers_breast["density"]:
        $ breast_score += 1
    if player_answers_breast["left_breast_calcifications"] == correct_answers_breast["left_breast_calcifications"]:
        $ breast_score += 1
    if player_answers_breast["right_breast_calcifications"] == correct_answers_breast["right_breast_calcifications"]:
        $ breast_score += 1
    if player_answers_breast["left_breast_asymmetry"] == correct_answers_breast["left_breast_asymmetry"]:
        $ breast_score += 1
    if player_answers_breast["right_breast_asymmetry"] == correct_answers_breast["right_breast_asymmetry"]:
        $ breast_score += 1
    if player_answers_breast["left_breast_mass"] == correct_answers_breast["left_breast_mass"]:
        $ breast_score += 1
    if player_answers_breast["right_breast_mass"] == correct_answers_breast["right_breast_mass"]:
        $ breast_score += 1

    $ total_score = breast_score + chole_score + div_score + appy_score

    $ menu_visible = False
    h "Let's review your report."

    jump density_breast

# End of breast case
label end_breast:
    scene bg readingroom
    h "You have completed this case. Let's see how you did."
    h "You scored [breast_score] out of 14."

    $ physical_text = ""
    $ vitals_text = ""
    $ show_physical = False
    $ show_vitals = False
    $ show_notification = False
    hide screen DICOMViewer
    # $ breast_var = False  # Disable this case for future runs

    jump start

label density_breast:
    # Review breast density report section
    scene bg readingroom
    h "Let's start with breast density."
    h "You reported the breast tissue as: [player_answers_breast['density']]"
    if player_answers_breast["density"] == correct_answers_breast["density"]:
        h "Great job, the density is heterogeneously dense."
    else:
        h "Incorrect. The density is heterogeneously dense, but you reported: [player_answers_breast['density']]"
    image breast density chart = "breast/breast_density_chart.png"
    show breast density chart at right_middle
    h "Breast tissue density is organized into categories A-D."
    h "A: Almost entirely fatty, B: Scattered fibroglandular densities, C: Heterogeneously dense, D: Extremely dense."
    h "When breasts are heterogeneously dense it may obscure small masses."
    hide breast density chart

    jump left_breast_calcifications

label left_breast_calcifications:
    h "Now, let's examine the left breast for calcifications."
    h "You reported the left breast calcifications as: [player_answers_breast['left_breast_calcifications']]"
    if player_answers_breast["left_breast_calcifications"] == correct_answers_breast["left_breast_calcifications"]:
        h "Great job, the left breast has no calcifications."
    else:
        h "Incorrect. The left breast has no calcifications, but you reported: [player_answers_breast['left_breast_calcifications']]"

    jump right_breast_calcifications

label right_breast_calcifications:
    h "Now, let's examine the right breast for calcifications."
    h "You reported the right breast calcifications as: [player_answers_breast['right_breast_calcifications']]"
    if player_answers_breast["right_breast_calcifications"] == correct_answers_breast["right_breast_calcifications"]:
        h "Great job, the right breast has benign appearing calcifications."
    else:
        h "Incorrect. The right breast has benign appearing calcifications, but you reported: [player_answers_breast['right_breast_calcifications']]"
    h "Can you identify where the majority of the calcifications are in the right breast?"
    call screen breast_calcifications_image_minigame()

screen breast_calcifications_image_minigame():
    default error_message = ""
    default screen_tooltip = ""
    zorder 100
    frame:
        xalign 0.9
        yalign 0.5
        xsize 550
        ysize 600

        add "breast/breast_calcs.png"
        modal True

        # Calcifications button
        if not selected_calcs:
            imagebutton auto "breast/breast_calcs_calcs_%s.png":
                focus_mask True
                hovered SetScreenVariable("screen_tooltip", "Click to select.")
                unhovered SetScreenVariable("screen_tooltip", "")
                action [
                    SetScreenVariable("selected_calcs", True),
                    Jump("correct_calcs_image")
                ]

        # Incorrect buttons
        imagebutton auto "breast/breast_calcs_inc1_%s.png":
            focus_mask True
            hovered SetScreenVariable("screen_tooltip", "Click to select.")
            unhovered SetScreenVariable("screen_tooltip", "")
            action [
                SetScreenVariable("error_message", "Incorrect. Try again."),
                Function(lambda: setattr(store, "breast_score", breast_score - 1)),
                Function(lambda: setattr(store, "total_score", appy_score + chole_score + div_score + breast_score)),
                Function(renpy.restart_interaction),
            ]

        imagebutton auto "breast/breast_calcs_inc2_%s.png":
            focus_mask True
            hovered SetScreenVariable("screen_tooltip", "Click to select.")
            unhovered SetScreenVariable("screen_tooltip", "")
            action [
                SetScreenVariable("error_message", "Incorrect. Try again."),
                Function(lambda: setattr(store, "breast_score", breast_score - 1)),
                Function(lambda: setattr(store, "total_score", appy_score + chole_score + div_score + breast_score)),
                Function(renpy.restart_interaction),
            ]

        if error_message:
            text "[error_message]" color "#f00" xalign 0.5 yalign 0.90
            timer 2.0 action SetScreenVariable("error_message", "") repeat False

        if screen_tooltip:
            text "[screen_tooltip]" color "#fff" xalign 0.5 yalign 0.98

        # Show continue only after both correct have been selected
        if selected_calcs:
            textbutton "Continue" action Jump("after_breast_minigame") xalign 0.5 yalign 0.95

label correct_calcs_image:
    hide screen breast_calcifications_image_minigame
    scene bg readingroom
    $ breast_score += 1
    $ total_score = appy_score + chole_score + div_score + breast_score
    $ selected_calcs = True
    h "Great job! How would you describe these calcifications?"
    call screen breast_menu

    jump after_breast_minigame

screen breast_menu():
    frame:
        xalign 1.0
        yalign 0.2
        xsize 700  # Set a fixed width for a more vertical look
        ypadding 40
        vbox:
            spacing 20  # Adds space between buttons
            text "How would you describe these calcifications?" xalign 0.5
            textbutton "Diffuse skin calcifications" action Jump("breast_calc_incorrect") xalign 0.5
            textbutton "Vascular breast calcifications" action Jump("breast_calc_incorrect") xalign 0.5
            textbutton "Coarse “popcorn-like” calcifications" action Jump("breast_calc_incorrect") xalign 0.5
            textbutton "Scattered punctate calcifications" action [SetVariable("breast_score", breast_score + 1), Jump("breast_calc_correct_menu")] xalign 0.5

label breast_calc_incorrect:
    scene bg readingroom    
    h "Incorrect. This is not the correct description for the calcifications."
    $ breast_score -= 1
    $ total_score = appy_score + chole_score + div_score + breast_score
    call screen breast_menu

label breast_calc_correct_menu:
    $ total_score = appy_score + chole_score + div_score + breast_score
    scene bg readingroom    
    image breast calcifications arrow = "breast/calcifications_arrow@2.jpg"
    image breast calcifications circle = "breast/calcifications_circle.png"
    h "Correct, these are benign-appearing scattered punctate calcifications."
    show breast calcifications arrow at right_middle
    h "Here is an example from another case."
    h "In the current BI-RADS edition, the term round encompasses both round and punctate."
    h "The assessment and management of round calcifications depends on distribution and if they are stable, new, and/or increasing."
    h "When they are diffuse, they may be dismissed as benign."
    hide breast calcifications arrow
    image breast calcifications spot = "breast/calcifications_spot.png"
    show breast calcifications spot at right_middle
    h "Spot magnification views show the calcifications in detail."
    hide breast calcifications spot
    
    jump left_breast_asymmetry

label left_breast_asymmetry:
    scene bg readingroom
    h "Now, let's examine the left breast for asymmetries."
    h "You reported the left breast asymmetries as: [player_answers_breast['left_breast_asymmetry']]"
    if player_answers_breast["left_breast_asymmetry"] == correct_answers_breast["left_breast_asymmetry"]:
        h "Great job, the left breast has an asymmetry."
    else:
        h "Incorrect. The left breast has an asymmetry, but you reported: [player_answers_breast['left_breast_asymmetry']]"
    h "There is an asymmetry in the medial left breast at middle depth."
    h "What is the next step you would like to take to evaluate this asymmetry?"
    call screen left_asymmetry_menu()

screen left_asymmetry_menu():
    frame:
        xalign 1.0
        yalign 0.2
        xsize 700  # Set a fixed width for a more vertical look
        ypadding 40
        vbox:
            spacing 20  # Adds space between buttons
            text "What is the next view for evaluation of this asymmetry?" xalign 0.5
            textbutton "No further evaluation" action Jump("left_asymmetry_incorrect") xalign 0.5
            textbutton "Biopsy of the asymmetry" action Jump("left_asymmetry_incorrect") xalign 0.5
            textbutton "Compression tomosynthesis" action [SetVariable("breast_score", breast_score + 1), Jump("left_asymmetry_correct")] xalign 0.5
            textbutton "Ultrasound" action Jump("left_asymmetry_incorrect") xalign 0.5

label left_asymmetry_incorrect:
    scene bg readingroom    
    h "Incorrect. This is not the correct next step."
    $ breast_score -= 1
    $ total_score = appy_score + chole_score + div_score + breast_score
    call screen left_asymmetry_menu()

label left_asymmetry_correct:
    scene bg readingroom
    $ total_score = appy_score + chole_score + div_score + breast_score
    h "Correct! A compression tomosynthesis is the next best view."
    h "Note that over 80 percent of asymmetries are due to summation of normal tissues."
    h "Spot compression and magnification techniques can be used to spread tissues apart."
    image left cc tomo = "breast/left_cc_tomo.png"
    show left cc tomo at right_middle
    h "Here is the left CC tomosynthesis image."
    h "The asymmetry is still visible with compression."
    h "What would be the next best step to further evaluate this asymmetry?"
    hide left cc tomo
    call screen left_asymmetry_menu_2()

screen left_asymmetry_menu_2():
    frame:
        xalign 1.0
        yalign 0.2
        xsize 700  # Set a fixed width for a more vertical look
        ypadding 40
        vbox:
            spacing 20  # Adds space between buttons
            text "What is the next view for evaluation of this asymmetry?" xalign 0.5
            textbutton "No further evaluation" action Jump("left_asymmetry_incorrect_2") xalign 0.5
            textbutton "Biopsy of the asymmetry" action Jump("left_asymmetry_incorrect_2") xalign 0.5
            textbutton "MRI" action Jump("left_asymmetry_incorrect_2") xalign 0.5
            textbutton "Ultrasound" action [SetVariable("breast_score", breast_score + 1), Jump("left_asymmetry_correct_2")] xalign 0.5

label left_asymmetry_incorrect_2:
    scene bg readingroom    
    h "Incorrect. This is not the correct next step."
    $ breast_score -= 1
    $ total_score = appy_score + chole_score + div_score + breast_score
    call screen left_asymmetry_menu_2()

label left_asymmetry_correct_2: 
    scene bg readingroom
    $ can_move_to_left_asymmetry_menu = True
    $ total_score = appy_score + chole_score + div_score + breast_score
    h "Correct! An ultrasound is the next best step."
    h "Ultrasound can help characterize the asymmetry further."
    image left asymmetry ultrasound = "breast/left_asymmetry_us.png"
    show left asymmetry ultrasound at right_middle
    h "Targeted ultrasound demonstrates a 5 mm oval circumscribed hypoechoic mass at 10:00, 3 cm from the nipple."
    h "This correlates with mammographic findings."
    h "This well defined, oval, hypoechoic mass is low suspicion for malignancy."
    hide left asymmetry ultrasound
    jump right_breast_asymmetry

label right_breast_asymmetry:
    scene bg readingroom
    h "Now, let's examine the right breast for asymmetries."
    h "You reported the right breast asymmetries as: [player_answers_breast['right_breast_asymmetry']]"
    if player_answers_breast["right_breast_asymmetry"] == correct_answers_breast["right_breast_asymmetry"]:
        h "Great job, the right breast has a focal asymmetry."
    else:
        h "Incorrect. The right breast has a focal asymmetry, but you reported: [player_answers_breast['right_breast_asymmetry']]"
    image right asymmetry mag = "breast/right_asymmetry_mag.png"
    image right asymmetry compression = "breast/right_asymmetry_compression.png"
    image right asymmetry us = "breast/right_asymmetry_us.png"
    show right asymmetry mag at right_middle
    h "There is a focal asymmetry in the upper outer quadrant of the right breast."
    h "Focal asymmetry is a relatively small area of fibroglandular tissue density involving less than a quadrant of the breast and seen in two different projections."
    h "In contrast to the convex countours of a mass a focal asymmetry will display concave contours."
    h "The workup here is similar to the left breast."
    hide right asymmetry mag
    show right asymmetry compression at right_middle
    h "Spot compression can help to better visualize the asymmetry and see if compression spreads tissue apart."
    hide right asymmetry compression
    show right asymmetry us at right_middle
    h "Ultrasound can help characterize the asymmetry further."
    h "Targeted ultrasound demonstrates a 1.1 cm oval circumscribed hypoechoic mass at 11:00, 6 cm from the nipple."
    hide right asymmetry us
    
    call screen right_asymmetry_menu()

screen right_asymmetry_menu():
    frame:
        xalign 1.0
        yalign 0.2
        xsize 700  # Set a fixed width for a more vertical look
        ypadding 40
        vbox:
            spacing 20  # Adds space between buttons
            text "What is the next step for the evaluation of this asymmetry?" xalign 0.5
            textbutton "No further evaluation" action Jump("right_asymmetry_incorrect") xalign 0.5
            textbutton "Biopsy of the asymmetry" action [SetVariable("breast_score", breast_score + 1), Jump("right_asymmetry_correct")] xalign 0.5
            textbutton "Thermography" action Jump("right_asymmetry_incorrect") xalign 0.5
            textbutton "MRI" action Jump("right_asymmetry_incorrect") xalign 0.5

label right_asymmetry_incorrect:
    scene bg readingroom    
    h "Incorrect. This is not the correct next step."
    $ breast_score -= 1
    $ total_score = appy_score + chole_score + div_score + breast_score
    call screen right_asymmetry_menu()

label right_asymmetry_correct:
    h "Correct an ultrasound-guided core biopsy is recommended."
    h "Now that the location of the asymmetry has been established in the breast and has been identified in more than one view, it may be categorized as a mass."
    h "Note in contrast to the asymmetry in the right breast this mass is larger and irregular in shape."

    jump left_breast_mass

label left_breast_mass:
    scene bg readingroom
    h "Now, let's examine the left breast for masses."
    h "You reported the left breast mass as: [player_answers_breast['left_breast_mass']]"
    if player_answers_breast["left_breast_mass"] == correct_answers_breast["left_breast_mass"]:
        h "Great job, the left breast has suspicious masses."
    else:
        h "Incorrect. The left breast has suspicious masses, but you reported: [player_answers_breast['left_breast_mass']]"
    image left breast mass posterior = "breast/left_breast_mass_posterior.png"
    show left breast mass posterior at right_middle
    h "There is an oval mass with irregular margins in the posterior central left breast."
    hide left breast mass posterior
    image left breast mass posterior us = "breast/left_breast_mass_posterior_us.png"
    show left breast mass posterior us at right_middle
    h "Targeted ultrasound demonstrates a 3.2 cm oval hypoechoic mass with irregular margins at 5:00, 3 cm from the nipple."
    h "This mass correlates with the patients palpable symptoms."
    hide left breast mass posterior us
    image left breast mass superior = "breast/left_breast_mass_superior.png"
    show left breast mass superior at right_middle
    h "There is also an oval circumscribed mass in the upper central left breast."
    image left breast mass superior us = "breast/left_breast_mass_superior_us.png"
    show left breast mass superior us at right_middle
    h "Targeted ultrasound demonstrates an 8 mm oval circumscribed predominantly hypoechoic mass in the left breast at 12:00, 4 cm from the nipple."
    hide left breast mass superior us
    image left breast axilla = "breast/left_breast_axilla.png"
    show left breast axilla at right_middle
    h "Finally, Targeted sonography of the left axilla reveals a 1.9 cm lymph node at 13 cm from the nipple."
    hide left breast axilla
    h "What is the next step for the evaluation of these masses?"

    call screen left_breast_mass_menu()

screen left_breast_mass_menu():
    frame:
        xalign 1.0
        yalign 0.2
        xsize 700  # Set a fixed width for a more vertical look
        ypadding 40
        vbox:
            spacing 20  # Adds space between buttons
            text "What is the next step for the evaluation of these masses?" xalign 0.5
            textbutton "No further evaluation" action Jump("left_breast_mass_incorrect") xalign 0.5
            textbutton "Biopsy of the masses" action [SetVariable("breast_score", breast_score + 1), Jump("left_breast_mass_correct")] xalign 0.5
            textbutton "Thermography" action Jump("left_breast_mass_incorrect") xalign 0.5
            textbutton "MRI" action Jump("left_breast_mass_incorrect") xalign 0.5

label left_breast_mass_incorrect:
    scene bg readingroom    
    h "Incorrect. This is not the correct next step."
    $ breast_score -= 1
    $ total_score = appy_score + chole_score + div_score + breast_score
    call screen left_breast_mass_menu()

label left_breast_mass_correct:
    h "Correct an ultrasound-guided core biopsy is recommended for all three of these masses."
    
    jump right_breast_mass

label right_breast_mass:
    scene bg readingroom
    h "Now, let's examine the right breast for masses."
    h "You reported right breast mass as: [player_answers_breast['right_breast_mass']]"
    if player_answers_breast["right_breast_mass"] == correct_answers_breast["right_breast_mass"]:
        h "Great job, the right breast does not have a mass visible on mammogram."
    else:
        h "Incorrect. The right breast has no mass visible on mammogram, but you reported: [player_answers_breast['right_breast_mass']]"
    h "However if you recall our exploration of the right sided asymmetry there is a right sided mass."
    h "Per US there is a 1.1 cm mass in the right breast at 11:00, 6 cm from the nipple that is low suspicion for malignancy."
    h "An ultrasound-guided core biopsy is recommended."


label birads:
    h "Let's explore why we are going to biopsy these masses."
    image diagnostic workup = "breast/diagnostic_workup@4.jpg"
    image acr criteria = "breast/acr_criteria@1.5.png"
    h "Following the ACR criteria and diagnostic work-up workflow for this patient we can follow this train of thought logically."
    show acr criteria at right_middle
    h "For a 37 yo patient w/ a palpable mass a diagnostic mammogram with ultrasound and tomosynthesis is indicated."
    hide acr criteria
    show diagnostic workup at right_upper
    h "However, our patient was brought back due to abnormal findings on a screening mammogram."
    h "With judicious use of ultrasound and spot compression views we can systematically rule out common benign findings."
    h "Our patient's findings can be described with BI-RADS terminology that raises suspicion for malignancy."
    hide diagnostic workup
    call screen birads_menu()

    screen birads_menu():
        frame:
            xalign 1.0
            yalign 0.2
            xsize 700  # Set a fixed width for a more vertical look
            ypadding 40
            vbox:
                spacing 20  # Adds space between buttons
                text "What is the BI-RADS category for this patient?" xalign 0.5
                textbutton "0" action Jump("birads_incorrect") xalign 0.5
                textbutton "1" action Jump("birads_incorrect") xalign 0.5
                textbutton "2" action Jump("birads_incorrect") xalign 0.5
                textbutton "3" action Jump("birads_incorrect") xalign 0.5
                textbutton "4" action Jump("birads_correct") xalign 0.5
                textbutton "5" action Jump("birads_incorrect") xalign 0.5

label birads_incorrect:
    scene bg readingroom    
    h "Incorrect. This is not the correct next BI-RADS category."
    $ breast_score -= 1
    $ total_score = appy_score + chole_score + div_score + breast_score
    call screen birads_menu()

label birads_correct:
    $ breast_score += 1
    $ total_score = appy_score + chole_score + div_score + breast_score
    image birads category = "breast/birads_categories.png"
    show birads category at right_middle
    h "Correct! This patient's findings are consistent with a BI-RADS 4 category: Suspicious Abnormality - Biopsy Should Be Considered."
    h "Specifically, due to the presence of a new indistinct irregular solitary mass, our patient is BIRADS 4C."
    
    h "Would you like to restart the case or return to the main menu?"
    menu:
        "Restart Case":
            jump breast_case_1

        "Return to Main Menu":
            jump end_breast
