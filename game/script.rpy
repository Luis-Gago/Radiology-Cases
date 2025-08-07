# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define a = Character("Dr. Levine", image="DrLevine", color="#c70909c1")
define l = Character("Luis Gago", image="LuisGago", color="#c70909c1")
image side DrLevine = "DrLevine.png"
image side LuisGago = "LuisGago@1.5.png"

# Declare score
default total_score = 0
default appy_score = 0
default chole_score = 0
default div_score = 0

#Define case variables 
default appendicitis_var = True
default cholecystitis_var = True
default diverticulitis_var = True

#Menu Variable definitions
default menu_visible = False
default menu_notification = False
default dynamic_content = ""
default physical_text = ""
default vitals_text = ""
default labs_text = ""
default show_physical = False
default show_vitals = False 
default show_labs = False
default physical_visible = False
default vitals_visible = False  
default labs_visible = False


# Default values for player answers
default player_answers_appy = {"liver": "", "chest": "", "appendix": "", "kidney": "", "gallbladder": "", "bones": ""}
default player_answers_chole = {"bones": "", "liver": "", "chest": "", "pancreas": "", "kidney": "", "gallbladder": "", "bodywall": "", "GI_tract": ""}
default player_answers_div = {"liver": "", "chest": "", "appendix": "", "kidney": "", "gallbladder": "", "bones": ""}

# Variables for grading appendicitis case
default correct_answers_appy = {"liver": "Benign finding noted.", "chest": "Benign finding noted.", "appendix": "Pathological finding present.", "kidney": "Pathological finding present.", "gallbladder": "Normal.", "bones": "Normal."}

# Variables for grading cholecystitis case
default correct_answers_chole = {"bones": "Normal.", "liver": "Normal.", "chest": "Benign finding noted.", "pancreas": "Normal.", "kidney": "Benign finding noted.", "gallbladder": "Pathological finding present.", "bodywall": "Benign finding noted.", "GI_tract": "Benign finding noted."}

# Variables for grading diverticulitis case
default correct_answers_div = {"liver": "", "chest": "", "appendix": "", "kidney": "", "gallbladder": "", "bones": ""}    

# Display images at right middle
transform right_middle:
    xalign 1.0
    yalign 0.5

# The game starts here.

label start:

    # Set the dynamic content for the EHR menu
    $ dynamic_content = "No information available."
    $ total_score = appy_score + chole_score + div_score

    # Show a background. 
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.
    scene bg emergency

    #Load the menu
    show screen persistent_menu

    menu:
        "Welcome to Radiology Case Simulator. \n Please select a topic."

        "Emergency Cases":
            jump emergency_cases
        "About":
            jump about
        # "Breast Imaging":
        #     jump breast_imaging
    
    return

label emergency_cases:
    # Menu for emergency case selection
    menu:
        "Welcome to Emergency Radiology Case Simulator. \n Please select a case."

        "Case 1" if appendicitis_var == True:
            jump appendicitis
        "Case 2" if cholecystitis_var == True:
            jump cholecystitis
        # "Case 3" if diverticulitis_var == True:
        #     jump diverticulitis
        "Main Menu":
            jump start
        "Citations":
            jump citations_emergency

label citations_emergency:
    scene bg readingroom
    l "Citations for Emergency Cases:"
    l "Emergency Cases presented by Luis Gago, MS4 at Northwestern Feinberg School of Medicine"
    jump start

label about:
    scene bg readingroom
    l "The Radiology Case Simulator was created by Luis Gago, an MS4 at Feinberg School of Medicine."
    l "RCS was made using Ren'Py: https://www.renpy.org/ and is hosted on Github: https://github.com/"
    l "You may view the source code here: https://github.com/Luis-Gago/Radiology-Cases/"

# label breast_imaging:
#     # Menu for breast imaging case selection
#     menu:
#         "Welcome to Breast Imaging Case Simulator. \n Please select a case."

#         "Case 1":
#             jump breast_case_1
#         "Case 2":
#             jump breast_case_2
#         "Main Menu":
#             jump start
#         "Citations":
#             jump citations_breast