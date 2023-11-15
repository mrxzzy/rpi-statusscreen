#!/usr/bin/python

import epdlib

# basic layout structure with two blocks
llayout = {
    'text_block': {
        'type':            'TextBlock',
        'height':          .5,
        'width':           1,
        'max_lines':       4,
        'abs_coordinates': (0, 0),
        'padding':         10,
        'text_wrap':       True,
        'fill':            'BLACK',
        'bkground':        'WHITE',
        'font': './resources/fhwa-series-d.otf',
        'border_config':   {'fill': 'BLACK', 'width': 5, 'sides': ['left', 'right']},
        'mode':            'L',

    },
    'image_block': {
        'type':            'ImageBlock',
        'height':          .5,
        'width':           1,
        'hcenter':         True,
        'vcenter':         False,
        'abs_coordinates': (0, None),
        # use absolute position declared in this block for the X
        # use the bottom of the text_block as the Y position for this block
        'relative':        ('image_block', 'text_block'),
        'bkground':        'WHITE',
        'fill':            'BLACK',
        'mode':            'L'
    }
}
# create a layout object that supports 8 bit gray
my_layout = epdlib.Layout(resolution=(350, 200), mode='L')
# assign the layout
my_layout.layout = llayout
# update the `text_block` and `image_block` with contents
my_layout.update_contents({'text_block':
                           'Jackdaws love my big sphinx of quartz. The quick brown fox jumps over the lazy dog.',
                          'image_block':
                            './resources/tux.png'})
# generate an image from all of the blocks joined together
img = my_layout.concat()
# save the image to a file
img.save('spam_image.jpg')
# update only the text
my_layout.update_contents({'text_block':
                           'The jay, pig, fox, zebra and my wolves quack!'})
img = my_layout.concat()
img.save('ham_image.jpg')
