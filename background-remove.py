from gimpfu import *

def python_remove_background(image, drawable):
    # Start a new undo group
    pdb.gimp_undo_push_group_start(image)

    # Duplicate the layer
    layer_copy = drawable.copy()
    image.add_layer(layer_copy, 0)

    # Convert the layer to grayscale
    pdb.gimp_image_convert_grayscale(image)

    # Apply the Sobel edge detection algorithm
    pdb.plug_in_sobel(image, layer_copy, TRUE, TRUE)

    # Threshold the layer to create a mask
    pdb.gimp_threshold(layer_copy, 128, 255)

    # Invert the mask
    pdb.gimp_invert(layer_copy)

    # Apply the mask to the original layer
    layer_mask = layer_copy.create_mask(ADD_WHITE_MASK)
    drawable.add_mask(layer_mask)

    # Remove the background
    pdb.gimp_edit_clear(drawable)

    # Apply the changes and finish the undo group
    drawable.remove_mask(MASK_APPLY)
    image.remove_layer(layer_copy)
    pdb.gimp_undo_push_group_end(image)

    # Update the display
    gimp.displays_flush()

register(
    "python_fu_remove_background",
    "Remove Background",
    "Attempts to remove the background of an image by detecting the edges of the foreground",
    "Austin Wilcox",
    "gutter-bravado",
    "2024",
    "<Image>/Filters/Custom/Remove Background...",
    "*",
    [],
    [],
    python_remove_background)

main()
