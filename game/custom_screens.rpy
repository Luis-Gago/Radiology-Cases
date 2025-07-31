init python:
    class DICOMSlidingCache:
        def __init__(self, window_size=8):  # Increased window size
            self.cache = set()
            self.window_size = window_size
            self.current_images = []
            
        def preload_around_index(self, current_index, image_list):
            # Store current image list
            self.current_images = image_list
            
            # Calculate range to preload (larger window)
            start = max(0, current_index - self.window_size)
            end = min(len(image_list), current_index + self.window_size + 1)
            
            # Preload images in sliding window
            new_cache = set()
            for i in range(start, end):
                if i < len(image_list):
                    img_path = image_list[i]
                    new_cache.add(img_path)
                    if img_path not in self.cache:
                        try:
                            # Multiple preloading strategies
                            renpy.cache_pin(img_path)
                            # Force load the image immediately
                            renpy.loadable(img_path)
                            # Try to get the displayable
                            d = renpy.displayable(img_path)
                            if d:
                                d.load()
                        except Exception as e:
                            pass
            
            # Clean up old cached images
            to_remove = self.cache - new_cache
            for img in to_remove:
                try:
                    renpy.cache_unpin(img)
                except:
                    pass
            
            self.cache = new_cache
        
        def preload_all_sets(self, all_image_sets, start_index=0):
            """Preload initial images from all sets for faster switching"""
            for image_set in all_image_sets:
                for i in range(start_index, min(len(image_set), start_index + 10)):  # Preload more images
                    try:
                        renpy.cache_pin(image_set[i])
                        renpy.loadable(image_set[i])
                        d = renpy.displayable(image_set[i])
                        if d:
                            d.load()
                    except:
                        pass
        
        def aggressive_preload(self, image_list, start_idx, count=20):
            """Aggressively preload a range of images"""
            end_idx = min(len(image_list), start_idx + count)
            for i in range(start_idx, end_idx):
                try:
                    img_path = image_list[i]
                    renpy.cache_pin(img_path)
                    renpy.loadable(img_path)
                    # Force immediate load
                    d = renpy.displayable(img_path)
                    if hasattr(d, 'load'):
                        d.load()
                    self.cache.add(img_path)
                except:
                    pass

    # Global cache for DICOM images - shared across all cases
    dicom_cache = DICOMSlidingCache(window_size=20)


# DICOM Viewer screen
screen DICOMViewer(images, image_sets=None, current_set=0, set_names=None):

    default dicom_index = 0
    
    # Initialize cache when screen is shown
    on "show" action Function(dicom_cache.preload_around_index, 0, images)

    # Keyboard and mouse wheel navigation with cache preloading
    key "K_UP" action If(dicom_index > 0, [
        SetScreenVariable("dicom_index", dicom_index - 1),
        Function(dicom_cache.preload_around_index, dicom_index - 1, images)
    ])
    key "K_DOWN" action If(dicom_index < len(images) - 1, [
        SetScreenVariable("dicom_index", dicom_index + 1),
        Function(dicom_cache.preload_around_index, dicom_index + 1, images)
    ])

    # Mouse wheel navigation with cache preloading
    key "mouseup_4" action If(dicom_index > 0, [
        SetScreenVariable("dicom_index", dicom_index - 1),
        Function(dicom_cache.preload_around_index, dicom_index - 1, images)
    ])
    key "mouseup_5" action If(dicom_index < len(images) - 1, [
        SetScreenVariable("dicom_index", dicom_index + 1),
        Function(dicom_cache.preload_around_index, dicom_index + 1, images)
    ])

    frame:
        style "menu_content_frame"
        xalign 0.35
        yalign 0.0
        vbox:
            text "PACS" style "menu_header"
            
            hbox:
                spacing 10
                textbutton "Prev" action If(dicom_index > 0, [
                    SetScreenVariable("dicom_index", dicom_index - 1),
                    Function(dicom_cache.preload_around_index, dicom_index - 1, images)
                ], NullAction()) text_color "#FFD600"
                text "[dicom_index + 1] / [len(images)]"
                textbutton "Next" action If(dicom_index < len(images) - 1, [
                    SetScreenVariable("dicom_index", dicom_index + 1),
                    Function(dicom_cache.preload_around_index, dicom_index + 1, images)
                ]) text_color "#FFD600"
            if image_sets is not None:
                hbox:
                    spacing 10
                    textbutton "Previous View" action [
                        SetScreenVariable("dicom_index", 0),
                        Function(dicom_cache.preload_around_index, 0, image_sets[(current_set-1)%len(image_sets)]),
                        Show("DICOMViewer", images=image_sets[(current_set-1)%len(image_sets)], image_sets=image_sets, current_set=(current_set-1)%len(image_sets), set_names=set_names)
                    ] text_color "#FFD600"
                    if set_names is not None:
                        text "[set_names[current_set]] ([current_set + 1] / [len(image_sets)])"
                    else:
                        text "Set [current_set + 1] / [len(image_sets)]"
                    textbutton "Next View" action [
                        SetScreenVariable("dicom_index", 0),
                        Function(dicom_cache.preload_around_index, 0, image_sets[(current_set+1)%len(image_sets)]),
                        Show("DICOMViewer", images=image_sets[(current_set+1)%len(image_sets)], image_sets=image_sets, current_set=(current_set+1)%len(image_sets), set_names=set_names)
                    ] text_color "#FFD600"

            # --- Move the slider bar OUTSIDE the viewport ---
            bar:
                value ScreenVariableValue("dicom_index", range=len(images) - 1)
                style "slider"
                xalign 0.5
                xmaximum 768
                # Add action when slider changes
                changed Function(dicom_cache.preload_around_index, dicom_index, images)

            viewport:
                scrollbars "vertical"
                xalign 0.5
                yalign 0.5
                xmaximum 768
                ymaximum 900  # Adjust as needed for your layout

                fixed:
                    xalign 0.5
                    yalign 0.5
                    xmaximum 768
                    yfit True
                    add images[dicom_index] zoom 1.5 xalign 0.5

#Code for a persistent menu in a Ren'Py game
screen persistent_menu():
    zorder 1000
    modal False
    
    fixed:
        xpos 25
        ypos 25
        xmaximum 360
        
        button:
            style "menu_header_button"
            action ToggleVariable("menu_visible")
            hbox:
                text "EHR" style "menu_header"
                if menu_notification:
                    text " (!)" color "#FF0000"
                text " Score: [total_score]" color "#FFD600"
                    
        
        if menu_visible:
            frame:
                style "menu_content_frame"
                ypos 40
                vbox:
                    spacing 5
                    text "[dynamic_content]"
                    if show_physical:
                        textbutton "Physical" action [ToggleVariable("physical_visible"), SetVariable("menu_notification", False)] text_color "#FFD600"
                    if show_vitals:
                        textbutton "Vitals" action [ToggleVariable("vitals_visible"), SetVariable("menu_notification", False)] text_color "#FFD600"
                    if show_labs:
                        textbutton "Labs" action [ToggleVariable("labs_visible"), SetVariable("menu_notification", False)] text_color "#FFD600"
                    
                    if physical_visible:
                        use Physical
                    if vitals_visible:
                        use Vitals
                    if labs_visible:
                        use Labs

style menu_header:
    size 24
    color "#FFFFFF"  # White text
    outlines [(1, "#000000", 0, 0)]  # Black outline
    hover_color "#FFFF00"  # Yellow when hovered
    yalign 0.5  # Vertical center
    xoffset 5  # Small left padding

    # Button style for the clickable header
style menu_header_button:
    xfill True
    ysize 40  # Fixed height
    background "#333"
    hover_background "#555"  # Darker when hovered
    padding (10, 0)

# Frame style for the dropdown content
style menu_content_frame:
    background "#3339"  # Semi-transparent dark
    padding (10, 10)

# Define the screens for Physical, Vitals, and Labs
screen Physical():
    frame:
        style "menu_content_frame"
        vbox:
            text "Physical Exam"
            text "[physical_text]"  # Use a variable for dynamic content

screen Vitals():
    frame:
        style "menu_content_frame"
        vbox:
            text "Vitals"
            text "[vitals_text]"  # Use a variable for dynamic content

screen Labs():
    frame:
        style "menu_content_frame"
        vbox:
            text "Labs"
            text "[labs_text]"  # Use a variable for dynamic content

# Style for the small text used in the Radiology Report appy screen
style small_text:
    size 30  # You can adjust this value to your preference

# Radiology Report screen for Appendicitis
screen RadiologyReportAppendicitis():

    default liver_status = ""
    default chest_status = ""
    default appendix_status = ""
    default kidney_status = ""
    default gallbladder_status = ""
    default bones_status = ""

    frame:
        style "menu_content_frame"
        xalign 1.0
        yalign 0.0
        xmaximum 700
        xfill True
        vbox:
            spacing 0
            xmaximum 700
            xfill True

            text "Radiology Report" style "menu_header"

            text "Bones:" style "small_text"
            text "[bones_status]" style "small_text"
            hbox:
                spacing 5
                textbutton "Normal" action [SetScreenVariable("bones_status", "Normal."), Function(player_answers_appy.__setitem__, 'bones', "Normal.")] text_color "#4CAF50" text_style "small_text"
                textbutton "Benign finding" action [SetScreenVariable("bones_status", "Benign finding noted."), Function(player_answers_appy.__setitem__, 'bones', "Benign finding noted.")] text_color "#2196F3" text_style "small_text"
                textbutton "Pathological finding" action [SetScreenVariable("bones_status", "Pathological finding present."), Function(player_answers_appy.__setitem__, 'bones', "Pathological finding present.")] text_color "#F44336" text_style "small_text"

            text "Chest:" style "small_text"
            text "[chest_status]" style "small_text"
            hbox:
                spacing 5
                textbutton "Normal" action [SetScreenVariable("chest_status", "Normal."), Function(player_answers_appy.__setitem__, 'chest', "Normal.")] text_color "#4CAF50" text_style "small_text"
                textbutton "Benign finding" action [SetScreenVariable("chest_status", "Benign finding noted."), Function(player_answers_appy.__setitem__, 'chest', "Benign finding noted.")] text_color "#2196F3" text_style "small_text"
                textbutton "Pathological finding" action [SetScreenVariable("chest_status", "Pathological finding present."), Function(player_answers_appy.__setitem__, 'chest', "Pathological finding present.")] text_color "#F44336" text_style "small_text"

            text "Liver:" style "small_text"
            text "[liver_status]" style "small_text"
            hbox:
                spacing 5
                textbutton "Normal" action [SetScreenVariable("liver_status", "Normal."), Function(player_answers_appy.__setitem__, 'liver', "Normal.")] text_color "#4CAF50" text_style "small_text"
                textbutton "Benign finding" action [SetScreenVariable("liver_status", "Benign finding noted."), Function(player_answers_appy.__setitem__, 'liver', "Benign finding noted.")] text_color "#2196F3" text_style "small_text"
                textbutton "Pathological finding" action [SetScreenVariable("liver_status", "Pathological finding present."), Function(player_answers_appy.__setitem__, 'liver', "Pathological finding present.")] text_color "#F44336" text_style "small_text"

            text "Gallbladder/Pancreas:" style "small_text"
            text "[gallbladder_status]" style "small_text"
            hbox:
                spacing 5
                textbutton "Normal" action [SetScreenVariable("gallbladder_status", "Normal."), Function(player_answers_appy.__setitem__, 'gallbladder', "Normal.")] text_color "#4CAF50" text_style "small_text"
                textbutton "Benign finding" action [SetScreenVariable("gallbladder_status", "Benign finding noted."), Function(player_answers_appy.__setitem__, 'gallbladder', "Benign finding noted.")] text_color "#2196F3" text_style "small_text"
                textbutton "Pathological finding" action [SetScreenVariable("gallbladder_status", "Pathological finding present."), Function(player_answers_appy.__setitem__, 'gallbladder', "Pathological finding present.")] text_color "#F44336" text_style "small_text"

            text "Kidneys:" style "small_text"
            text "[kidney_status]" style "small_text"
            hbox:
                spacing 5
                textbutton "Normal" action [SetScreenVariable("kidney_status", "Normal."), Function(player_answers_appy.__setitem__, 'kidney', "Normal.")] text_color "#4CAF50" text_style "small_text"
                textbutton "Benign finding" action [SetScreenVariable("kidney_status", "Benign finding noted."), Function(player_answers_appy.__setitem__, 'kidney', "Benign finding noted.")] text_color "#2196F3" text_style "small_text"
                textbutton "Pathological finding" action [SetScreenVariable("kidney_status", "Pathological finding present."), Function(player_answers_appy.__setitem__, 'kidney', "Pathological finding present.")] text_color "#F44336" text_style "small_text"

            text "Appendix:" style "small_text"
            text "[appendix_status]" style "small_text"
            hbox:
                spacing 5
                textbutton "Normal" action [SetScreenVariable("appendix_status", "Normal."), Function(player_answers_appy.__setitem__, 'appendix', "Normal.")] text_color "#4CAF50" text_style "small_text"
                textbutton "Benign finding" action [SetScreenVariable("appendix_status", "Benign finding noted."), Function(player_answers_appy.__setitem__, 'appendix', "Benign finding noted.")] text_color "#2196F3" text_style "small_text"
                textbutton "Pathological finding" action [SetScreenVariable("appendix_status", "Pathological finding present."), Function(player_answers_appy.__setitem__, 'appendix', "Pathological finding present.")] text_color "#F44336" text_style "small_text"

            textbutton "Submit Report" action Return() text_color "#FFD600" text_style "small_text"


# Style for the small text used in the Radiology Report screen
style very_small_text:
    size 29  # You can adjust this value to your preference

# Radiology Report screen for Cholecystitis
screen RadiologyReportCholecystitis():

    default liver_status = ""
    default chest_status = ""
    default GI_status = ""
    default kidney_status = ""
    default gallbladder_status = ""
    default pancreas_status = ""
    default bodywall_status = ""
    default bones_status = ""

    frame:
        style "menu_content_frame"
        xalign 1.0
        yalign 0.0
        xmaximum 700
        xfill True
        vbox:
            spacing 0
            xmaximum 700
            xfill True

            text "Radiology Report" style "menu_header"

            text "Bones:" style "very_small_text"
            text "[bones_status]" style "very_small_text"
            hbox:
                spacing 5 
                textbutton "Normal" action [SetScreenVariable("bones_status", "Normal."), Function(player_answers_chole.__setitem__, 'bones', "Normal.")] text_color "#4CAF50" text_style "very_small_text"
                textbutton "Benign finding" action [SetScreenVariable("bones_status", "Benign finding noted."), Function(player_answers_chole.__setitem__, 'bones', "Benign finding noted.")] text_color "#2196F3" text_style "very_small_text"
                textbutton "Pathological finding" action [SetScreenVariable("bones_status", "Pathological finding present."), Function(player_answers_chole.__setitem__, 'bones', "Pathological finding present.")] text_color "#F44336" text_style "very_small_text"

            text "Body wall:" style "very_small_text"
            text "[bodywall_status]" style "very_small_text"
            hbox:
                spacing 5
                textbutton "Normal" action [SetScreenVariable("bodywall_status", "Normal."), Function(player_answers_chole.__setitem__, 'bodywall', "Normal.")] text_color "#4CAF50" text_style "very_small_text"
                textbutton "Benign finding" action [SetScreenVariable("bodywall_status", "Benign finding noted."), Function(player_answers_chole.__setitem__, 'bodywall', "Benign finding noted.")] text_color "#2196F3" text_style "very_small_text"
                textbutton "Pathological finding" action [SetScreenVariable("bodywall_status", "Pathological finding present."), Function(player_answers_chole.__setitem__, 'bodywall', "Pathological finding present.")] text_color "#F44336" text_style "very_small_text"

            text "Chest:" style "very_small_text"
            text "[chest_status]" style "very_small_text"
            hbox:
                spacing 5
                textbutton "Normal" action [SetScreenVariable("chest_status", "Normal."), Function(player_answers_chole.__setitem__, 'chest', "Normal.")] text_color "#4CAF50" text_style "very_small_text"
                textbutton "Benign finding" action [SetScreenVariable("chest_status", "Benign finding noted."), Function(player_answers_chole.__setitem__, 'chest', "Benign finding noted.")] text_color "#2196F3" text_style "very_small_text"
                textbutton "Pathological finding" action [SetScreenVariable("chest_status", "Pathological finding present."), Function(player_answers_chole.__setitem__, 'chest', "Pathological finding present.")] text_color "#F44336" text_style "very_small_text"

            text "Liver:" style "very_small_text"
            text "[liver_status]" style "very_small_text"
            hbox:
                spacing 5
                textbutton "Normal" action [SetScreenVariable("liver_status", "Normal."), Function(player_answers_chole.__setitem__, 'liver', "Normal.")] text_color "#4CAF50" text_style "very_small_text"
                textbutton "Benign finding" action [SetScreenVariable("liver_status", "Benign finding noted."), Function(player_answers_chole.__setitem__, 'liver', "Benign finding noted.")] text_color "#2196F3" text_style "very_small_text"
                textbutton "Pathological finding" action [SetScreenVariable("liver_status", "Pathological finding present."), Function(player_answers_chole.__setitem__, 'liver', "Pathological finding present.")] text_color "#F44336" text_style "very_small_text"

            text "Gallbladder:" style "very_small_text"
            text "[gallbladder_status]" style "very_small_text"
            hbox:
                spacing 5
                textbutton "Normal" action [SetScreenVariable("gallbladder_status", "Normal."), Function(player_answers_chole.__setitem__, 'gallbladder', "Normal.")] text_color "#4CAF50" text_style "very_small_text"
                textbutton "Benign finding" action [SetScreenVariable("gallbladder_status", "Benign finding noted."), Function(player_answers_chole.__setitem__, 'gallbladder', "Benign finding noted.")] text_color "#2196F3" text_style "very_small_text"
                textbutton "Pathological finding" action [SetScreenVariable("gallbladder_status", "Pathological finding present."), Function(player_answers_chole.__setitem__, 'gallbladder', "Pathological finding present.")] text_color "#F44336" text_style "very_small_text"

            text "Pancreas:" style "very_small_text"
            text "[pancreas_status]" style "very_small_text"
            hbox:
                spacing 5
                textbutton "Normal" action [SetScreenVariable("pancreas_status", "Normal."), Function(player_answers_chole.__setitem__, 'pancreas', "Normal.")] text_color    "#4CAF50" text_style "very_small_text"
                textbutton "Benign finding" action [SetScreenVariable("pancreas_status", "Benign finding noted."), Function(player_answers_chole.__setitem__, 'pancreas', "Benign finding noted.")] text_color "#2196F3" text_style "very_small_text"  
                textbutton "Pathological finding" action [SetScreenVariable("pancreas_status", "Pathological finding present."), Function(player_answers_chole.__setitem__, 'pancreas', "Pathological finding present.")] text_color "#F44336" text_style "very_small_text"

            text "Kidneys:" style "very_small_text"
            text "[kidney_status]" style "very_small_text"
            hbox:
                spacing 5
                textbutton "Normal" action [SetScreenVariable("kidney_status", "Normal."), Function(player_answers_chole.__setitem__, 'kidney', "Normal.")] text_color "#4CAF50" text_style "very_small_text"
                textbutton "Benign finding" action [SetScreenVariable("kidney_status", "Benign finding noted."), Function(player_answers_chole.__setitem__, 'kidney', "Benign finding noted.")] text_color "#2196F3" text_style "very_small_text"
                textbutton "Pathological finding" action [SetScreenVariable("kidney_status", "Pathological finding present."), Function(player_answers_chole.__setitem__, 'kidney', "Pathological finding present.")] text_color "#F44336" text_style "very_small_text"

            text "GI Tract:" style "very_small_text"
            text "[GI_status]" style "very_small_text"
            hbox:
                spacing 5
                textbutton "Normal" action [SetScreenVariable("GI_status", "Normal."), Function(player_answers_chole.__setitem__, 'GI_tract', "Normal.")] text_color "#4CAF50" text_style "very_small_text"
                textbutton "Benign finding" action [SetScreenVariable("GI_status", "Benign finding noted."), Function(player_answers_chole.__setitem__, 'GI_tract', "Benign finding noted.")] text_color "#2196F3" text_style "very_small_text"
                textbutton "Pathological finding" action [SetScreenVariable("GI_status", "Pathological finding present."), Function(player_answers_chole.__setitem__, 'GI_tract', "Pathological finding present.")] text_color "#F44336" text_style "very_small_text"

            textbutton "Submit Report" action Return() text_color "#FFD600" text_style "very_small_text"




