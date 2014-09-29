# Copyright (c) 2013 phrack. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import canvas_manager
import pickle
from PIL import Image, ImageTk
from tag_parser import TagParser

class TargetPickler():
    def save(self, target_file, region_list, canvas):
        region_object = []

        for region in region_list:
            region_coords = canvas.coords(region)
            region_tags = canvas.gettags(region)
	
            if "_shape:image" in region_tags:
                region_object.append({"tags":region_tags,
                    "coords":region_coords})
            else:                
                region_fill = canvas.itemcget(region, "fill")
                region_object.append({"tags":region_tags,
                    "coords":region_coords,
                    "fill":region_fill})

        target = open(target_file, 'wb')
        pickle.dump(region_object, target, pickle.HIGHEST_PROTOCOL)
        target.close()

    # the target_name is set on every region in a target
    # and should be unique for the webcam feed so that
    # multiple instances of a target can exist
    def load(self, target_file, canvas, canvas_manager,
        image_regions_images, internal_target_name="_internal_name:target"):

        target = open(target_file, 'rb')
        region_object = pickle.load(target)
        target.close()

        regions = self._draw_target(region_object, canvas, canvas_manager,
                    image_regions_images, internal_target_name)
                
        return (region_object, regions)

    def _draw_target(self, region_object, canvas, _canvas_manager, 
        image_regions_images, internal_target_name):

        regions = []

        for region in region_object:
            shape = 0
            raw_tags = region["tags"]
    
            # Get rid of the default internal name otherwise every target
            # will have it and selection won't work
            raw_tags = tuple([value for value in raw_tags if value != "_internal_name:target"])

            raw_tags += (internal_target_name,)
            parsed_tags = TagParser.parse_tags(raw_tags)	

            if parsed_tags["_shape"] == "image":
                shape = canvas.create_image(region["coords"], image=None, 
                            tags=raw_tags)

                image = Image.open(parsed_tags["_path"])
                image_regions_images[shape] = (image, ImageTk.PhotoImage(image))

                canvas.itemconfig(shape, image=image_regions_images[shape][canvas_manager.PHOTOIMAGE_INDEX])

                _canvas_manager.animate(shape, parsed_tags["_path"], 
                    image_regions_images[shape][canvas_manager.PHOTOIMAGE_INDEX])

            if parsed_tags["_shape"] == "rectangle":
                shape = canvas.create_rectangle(region["coords"],
                    fill=region["fill"], stipple="gray25",
                    tags=raw_tags)

            if parsed_tags["_shape"] == "oval":
                shape = canvas.create_oval(region["coords"],
                    fill=region["fill"], stipple="gray25",
                    tags=raw_tags)

            if parsed_tags["_shape"] == "triangle":
                shape = canvas.create_polygon(region["coords"],
                    fill=region["fill"], outline="black",
                    stipple="gray25", tags=raw_tags)

            if parsed_tags["_shape"] == "aqt3":
                shape = canvas.create_polygon(region["coords"],
                    fill=region["fill"], outline="black",
                    stipple="gray25", tags=raw_tags)
                
            if parsed_tags["_shape"] == "aqt4":
                shape = canvas.create_polygon(region["coords"],
                    fill=region["fill"], outline="black",
                    stipple="gray25", tags=raw_tags)

            if parsed_tags["_shape"] == "aqt5":
                shape = canvas.create_polygon(region["coords"],
                    fill=region["fill"], outline="black",
                    stipple="gray25", tags=raw_tags)

            if parsed_tags["_shape"] == "freeform_polygon":
                shape = canvas.create_polygon(region["coords"],
                    fill=region["fill"], outline="black",
                    stipple="gray25", tags=raw_tags)

            if "visible" in parsed_tags and parsed_tags["visible"].lower() == "false":
                canvas.tag_lower(shape, "background")
            else:
                canvas.tag_raise(shape, "background")

            if shape != 0:
                regions.append(shape)

        return regions
