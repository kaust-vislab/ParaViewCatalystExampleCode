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
      # setup the data processing pipelines
      # ----------------------------------------------------------------

      #### disable automatic camera reset on 'Show'
      paraview.simple._DisableFirstRenderCameraReset()

      # create a new 'XML Partitioned Image Data Reader'
      # create a producer from a simulation input
      fullgrid_0pvti = coprocessor.CreateProducer(datadescription, 'input')

      # create a new 'Calculator'
      calculator1 = Calculator(Input=fullgrid_0pvti)
      calculator1.Function = 'mag(velocity)'

      # create a new 'Slice'
      slice1 = Slice(Input=calculator1)
      slice1.SliceType = 'Plane'
      slice1.SliceOffsetValues = [0.0]

      # init the 'Plane' selected for 'SliceType'
      slice1.SliceType.Origin = [512.0, 281.6, 332.8]
      slice1.SliceType.Normal = [-0.062350454622476334, -0.9100826022356976, -0.4097097483783753]

      # create a new 'Parallel PolyData Writer'
      parallelPolyDataWriter2 = servermanager.writers.XMLPPolyDataWriter(Input=slice1)

      # register the writer with coprocessor
      # and provide it with information such as the filename to use,
      # how frequently to write the data, etc.
      coprocessor.RegisterWriter(parallelPolyDataWriter2, filename='output.03/slice_%t.pvtp', freq=1)

      # create a new 'Stream Tracer'
      streamTracer1 = StreamTracer(Input=calculator1,
          SeedType='Point Source')
      streamTracer1.Vectors = ['POINTS', 'velocity']
      streamTracer1.MaximumStreamlineLength = 1024.0

      # init the 'Point Source' selected for 'SeedType'
      streamTracer1.SeedType.Center = [512.0, 281.6, 332.8]
      streamTracer1.SeedType.NumberOfPoints = 5000
      streamTracer1.SeedType.Radius = 512.0

      # create a new 'Parallel PolyData Writer'
      parallelPolyDataWriter1 = servermanager.writers.XMLPPolyDataWriter(Input=streamTracer1)

      # register the writer with coprocessor
      # and provide it with information such as the filename to use,
      # how frequently to write the data, etc.
      coprocessor.RegisterWriter(parallelPolyDataWriter1, filename='output.03/streamlines_%t.pvtp', freq=1)

    return Pipeline()

  class CoProcessor(coprocessing.CoProcessor):
    def CreatePipeline(self, datadescription):
      self.Pipeline = _CreatePipeline(self, datadescription)

  coprocessor = CoProcessor()
  # these are the frequencies at which the coprocessor updates.
  freqs = {'input': [1]}
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
