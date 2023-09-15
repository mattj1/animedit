# animedit
Flash-like 2D Animation editor intended for games.

UI is powered by PySide2/PyQt.


Basics =======
Selection
 
 - We can determine if a selection is a rilled rect if:
    - area of rectangle = # frames in selected array
    
 - When drawing a box in the frames view, the scrubber always follows the mouse
   - So, it's initially a "change selection" with an empty selection
   
   

- Need to figure out how to do selection. 

- Box selection / clicking: What is selected when you do this?

  - Selected tweened stuff can't be dragged unless the keyframe is selected

- Perhaps, on select, the frames involved should be highlighted in the timeline

- What happens when the scrubber moves?
    - This is a "Change Selection" action.
        - the action on the undo stack should be updated until the mouse button is released
        - Selected items are un-selected
        

- Right-clicking on timeline:
       - Inside selected frame(s):
          - brings up menu
          
       - on an unselected frame:
          - that frame is selected, then bring up menu

- Dragging tweened stuff is a special case

- With any frame create/convert:
  - play pointer should move to the right most of the frames being edited      
>>> clicking on item that's currently on a keyframe:
    - those frames are added to the selection
