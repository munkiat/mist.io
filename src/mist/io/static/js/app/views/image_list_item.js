define('app/views/image_list_item', ['app/views/list_item'],
    //
    //  Image List Item View
    //
    //  @returns Class
    //
    function (ListItemView) {

        'use strict';

        return ListItemView.extend({


            //
            //
            //  Properties
            //
            //


            image: null,


            //
            //
            //  Computed Properties
            //
            //


            starClass: function () {
                return this.image.star ? 'staron' : 'staroff';
            }.property('image.star'),


            //
            //
            //  Actions
            //
            //


            actions: {


                toggleImageStar: function () {
                    this.image.toggle();
                },


                launchImage: function () {
                    this.image.backend.images.content.addObject(this.image);
                    Mist.machineAddController.open();
                    Ember.run.next(this, function () {
                        Mist.machineAddController.view._actions.selectProvider(this.image.backend);
                        Mist.machineAddController.view._actions.selectImage(this.image);
                    });
                }
            }
        });
    }
);
