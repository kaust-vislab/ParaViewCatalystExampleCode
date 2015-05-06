from paraview.simple import *
from paraview import coprocessing


#--------------------------------------------------------------
# Code generated from cpstate.py to create the CoProcessor.
# ParaView 4.3.1-3-g784d16d 64 bits


# ----------------------- CoProcessor definition -----------------------

def CreateCoProcessor():
  def _CreatePipeline(coprocessor, datadescription):
    class Pipeline:
      # state file generated using paraview version 4.3.1-3-g784d16d

      # ----------------------------------------------------------------
      # setup views used in the visualization
      # ----------------------------------------------------------------

      #### disable automatic camera reset on 'Show'
      paraview.simple._DisableFirstRenderCameraReset()

      # Create a new 'Render View'
      renderView1 = CreateView('RenderView')
      renderView1.ViewSize = [1478, 1277]
      renderView1.CenterOfRotation = [512.0, 281.6000061035156, 332.79998779296875]
      renderView1.LightSwitch = 1
      renderView1.LightIntensity = 0.10000000000000014
      renderView1.StereoType = 0
      renderView1.CameraPosition = [2145.4949754880154, 1863.026185262708, -1839.5832309897244]
      renderView1.CameraFocalPoint = [561.9902679765646, 231.18822822801047, 331.3701883691208]
      renderView1.CameraViewUp = [-0.28712334606483636, 0.8545050847562522, 0.43287555286738305]
      renderView1.CameraParallelScale = 672.4569839867083
      renderView1.Background = [0.32, 0.34, 0.43]

      # register the view with coprocessor
      # and provide it with information such as the filename to use,
      # how frequently to write the images, etc.
      coprocessor.RegisterView(renderView1,
          filename='image_%t.png', freq=1, fittoscreen=0, magnification=1, width=1478, height=1277)

      # ----------------------------------------------------------------
      # setup the data processing pipelines
      # ----------------------------------------------------------------

      # create a new 'XML Partitioned Image Data Reader'
      # create a producer from a simulation input
      fullgrid_6pvti = coprocessor.CreateProducer(datadescription, 'input')

      # create a new 'Calculator'
      calculator1 = Calculator(Input=fullgrid_6pvti)
      calculator1.Function = 'mag(velocity)'

      # create a new 'Stream Tracer'
      streamTracer1 = StreamTracer(Input=calculator1,
          SeedType='Point Source')
      streamTracer1.Vectors = ['POINTS', 'velocity']
      streamTracer1.MaximumStreamlineLength = 1024.0

      # init the 'Point Source' selected for 'SeedType'
      streamTracer1.SeedType.Center = [512.0, 281.6, 332.8]
      streamTracer1.SeedType.NumberOfPoints = 1000
      streamTracer1.SeedType.Radius = 512.0

      # create a new 'Parallel PolyData Writer'
      parallelPolyDataWriter1 = servermanager.writers.XMLPPolyDataWriter(Input=streamTracer1)

      # register the writer with coprocessor
      # and provide it with information such as the filename to use,
      # how frequently to write the data, etc.
      coprocessor.RegisterWriter(parallelPolyDataWriter1, filename='streamlines_%t.pvtp', freq=1)

      # ----------------------------------------------------------------
      # setup color maps and opacity mapes used in the visualization
      # note: the Get..() functions create a new object, if needed
      # ----------------------------------------------------------------

      # get color transfer function/color map for 'velocity'
      velocityLUT = GetColorTransferFunction('velocity')
      velocityLUT.RGBPoints = [10.063513463551544, 0.278431, 0.278431, 0.858824, 12.132888722767962, 0.0, 0.0, 0.360784, 14.187792826325527, 0.0, 1.0, 1.0, 16.271639241200802, 0.0, 0.501961, 0.0, 18.326543344758363, 1.0, 1.0, 0.0, 20.39591860397478, 1.0, 0.380392, 0.0, 22.4652938631912, 0.419608, 0.0, 0.0, 24.53466912240762, 0.878431, 0.301961, 0.301961]
      velocityLUT.ColorSpace = 'RGB'
      velocityLUT.NanColor = [1.0, 1.0, 0.0]
      velocityLUT.ScalarRangeInitialized = 1.0

      # get opacity transfer function/opacity map for 'velocity'
      velocityPWF = GetOpacityTransferFunction('velocity')
      velocityPWF.Points = [10.063513463551544, 0.0, 0.5, 0.0, 24.53466912240762, 1.0, 0.5, 0.0]
      velocityPWF.ScalarRangeInitialized = 1

      # ----------------------------------------------------------------
      # setup the visualization in view 'renderView1'
      # ----------------------------------------------------------------

      # show data from fullgrid_6pvti
      fullgrid_6pvtiDisplay = Show(fullgrid_6pvti, renderView1)
      # trace defaults for the display properties.
      fullgrid_6pvtiDisplay.Representation = 'Outline'
      fullgrid_6pvtiDisplay.ColorArrayName = [None, '']
      fullgrid_6pvtiDisplay.ScalarOpacityUnitDistance = 2.084880721321322
      fullgrid_6pvtiDisplay.Slice = 256

      # show data from streamTracer1
      streamTracer1Display = Show(streamTracer1, renderView1)
      # trace defaults for the display properties.
      streamTracer1Display.ColorArrayName = ['POINTS', 'velocity']
      streamTracer1Display.LookupTable = velocityLUT

      # show color legend
      streamTracer1Display.SetScalarBarVisibility(renderView1, True)

      # setup the color legend parameters for each legend in this view

      # get color legend/bar for velocityLUT in view renderView1
      velocityLUTColorBar = GetScalarBar(velocityLUT, renderView1)
      velocityLUTColorBar.Title = 'velocity'
      velocityLUTColorBar.ComponentTitle = 'Magnitude'
    return Pipeline()

  class CoProcessor(coprocessing.CoProcessor):
    def CreatePipeline(self, datadescription):
      self.Pipeline = _CreatePipeline(self, datadescription)

  coprocessor = CoProcessor()
  # these are the frequencies at which the coprocessor updates.
  freqs = {'input': [1, 1, 1, 1]}
  coprocessor.SetUpdateFrequencies(freqs)
  return coprocessor

#--------------------------------------------------------------
# Global variables that will hold the pipeline for each timestep
# Creating the CoProcessor object, doesn't actually create the ParaView pipeline.
# It will be automatically setup when coprocessor.UpdateProducers() is called the
# first time.
coprocessor = CreateCoProcessor()

#--------------------------------------------------------------
# Enable Live-Visualizaton with ParaView
coprocessor.EnableLiveVisualization(False, 1)


# ---------------------- Data Selection method ----------------------

def RequestDataDescription(datadescription):
    "Callback to populate the request for current timestep"
    global coprocessor
    if datadescription.GetForceOutput() == True:
        # We are just going to request all fields and meshes from the simulation
        # code/adaptor.
        for i in range(datadescription.GetNumberOfInputDescriptions()):
            datadescription.GetInputDescription(i).AllFieldsOn()
            datadescription.GetInputDescription(i).GenerateMeshOn()
        return

    # setup requests for all inputs based on the requirements of the
    # pipeline.
    coprocessor.LoadRequestedData(datadescription)

# ------------------------ Processing method ------------------------

def DoCoProcessing(datadescription):
    "Callback to do co-processing for current timestep"
    global coprocessor

    # Update the coprocessor by providing it the newly generated simulation data.
    # If the pipeline hasn't been setup yet, this will setup the pipeline.
    coprocessor.UpdateProducers(datadescription)

    # Write output data, if appropriate.
    coprocessor.WriteData(datadescription);

    # Write image capture (Last arg: rescale lookup table), if appropriate.
    coprocessor.WriteImages(datadescription, rescale_lookuptable=False)

    # Live Visualization, if enabled.
    coprocessor.DoLiveVisualization(datadescription, "localhost", 22222)
