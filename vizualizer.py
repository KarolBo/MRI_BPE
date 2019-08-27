import numpy as np
from traits.api import HasTraits, Instance, Button, \
    on_trait_change
from traitsui.api import View, Item, HSplit, Group

from mayavi import mlab
from mayavi.core.ui.api import MlabSceneModel, SceneEditor


class MyDialog(HasTraits):

    scene1 = Instance(MlabSceneModel, ())
    scene2 = Instance(MlabSceneModel, ())

    data = np.random.rand(10,10,10)
    spacing = (1,1,1)
    categories = False

    def display(self):
        # Notice how each mlab call points explicitely to the figure it
        # applies to.
        mlab.clf(figure=self.scene1.mayavi_scene)
        mlab.clf(figure=self.scene2.mayavi_scene)

        class_a = self.data.copy()
        class_b = self.data.copy()
        class_c = self.data.copy()
        class_d = self.data.copy()
        class_a[:,:,self.categories!=0] = 0
        class_a[class_a<10]=0
        class_a[class_a>=10]=1
        class_b[:,:,self.categories!=1] = 0
        class_b[class_b<10]=0
        class_b[class_b>=10]=1
        class_c[:,:,self.categories!=2] = 0
        class_d[:,:,self.categories!=3] = 0

        if class_a.any():
            sfa = mlab.pipeline.scalar_field(class_a, figure=self.scene1.mayavi_scene)
            sfa.spacing = self.spacing
            mlab.pipeline.volume(sfa, figure=self.scene1.mayavi_scene, color=(0,1,0))

        if class_b.any():
            sfb = mlab.pipeline.scalar_field(class_b, figure=self.scene1.mayavi_scene)
            sfb.spacing = self.spacing
            mlab.pipeline.volume(sfb, figure=self.scene1.mayavi_scene, color=(0.8,0.8,0))

        if class_c.any():
            sfc = mlab.pipeline.scalar_field(class_c, figure=self.scene1.mayavi_scene)
            sfc.spacing = self.spacing
            mlab.pipeline.volume(sfc, figure=self.scene1.mayavi_scene, color=(0.9,0.6,0))

        if class_d.any():
            sfd = mlab.pipeline.scalar_field(class_d, figure=self.scene1.mayavi_scene)
            sfd.spacing = self.spacing
            mlab.pipeline.volume(sfd, figure=self.scene1.mayavi_scene, color=(1,0,0))

        sf = mlab.pipeline.scalar_field(self.data, figure=self.scene1.mayavi_scene)
        sf.spacing = self.spacing
        ipw = mlab.pipeline.image_plane_widget(sf, plane_orientation='z_axes')

        # sf2 = mlab.pipeline.scalar_field(self.data, figure=self.scene2.mayavi_scene)
        # sf2.spacing = self.spacing
        # outline = mlab.pipeline.outline(sf2, figure=self.scene2.mayavi_scene)
        # ipw2 = mlab.pipeline.image_plane_widget(outline, plane_orientation='z_axes')
        # ipw.ipw.sync_trait('slice_position', ipw2.ipw)

        ipw.ipw.add_observer('InteractionEvent', self.display_2)

        self.display_2()

    def display_2(self, obj=False, evt=False):
        if obj:
            obj.SetMarginSizeY(0)
            obj.SetMarginSizeX(0)
            slice_index = obj.GetSliceIndex()
        else:
            slice_index = 0
        mlab.imshow(self.data[:,:,slice_index], figure=self.scene2.mayavi_scene)

        print("Parenchyme enhancement class:", self.categories[slice_index])

    # The layout of the dialog created
    view = View(HSplit(
                  Group(
                       Item('scene1',
                            editor=SceneEditor(), height=250,
                            width=300),
                       show_labels=False,
                  ),
                  Group(
                       Item('scene2',
                            editor=SceneEditor(), height=250,
                            width=300, show_label=False),
                       show_labels=False,
                  ),
                ),
                resizable=True,
                )
