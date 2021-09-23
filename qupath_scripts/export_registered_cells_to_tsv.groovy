import static qupath.lib.gui.scripting.QPEx.* // For intellij editor autocompletion
import static ch.epfl.biop.qupath.atlas.allen.api.AtlasTools.*

import qupath.lib.objects.PathObjects
import qupath.lib.roi.ROIs
import qupath.lib.regions.ImagePlane
import qupath.lib.measurements.MeasurementList
import qupath.lib.objects.PathCellObject

import ch.epfl.biop.qupath.transform.*
import net.imglib2.RealPoint


// https://github.com/BIOP/qupath-biop-extensions/blob/master/src/test/resources/abba_scripts/importABBAResults.groovy
def targetEntry = getProjectEntry()
def targetEntryPath = targetEntry.getEntryPath();

def fTransform = new File (targetEntryPath.toString(),"ABBA-Transform.json")

if (!fTransform.exists()) {
    System.err.println("ABBA transformation file not found for entry "+targetEntry);
    return ;
}

def pixelToCCFTransform = Warpy.getRealTransform(fTransform).inverse(); // Needs the inverse transform


def imageData = getCurrentImageData();
imageName = ServerTools.getDisplayableImageName(imageData.getServer())

if (getCellObjects().isEmpty()) {
    throw new Exception("No cell detections in this file. Please run cell and subcellular spot detection on $imageName.")
}

getCellObjects().forEach{detection -> {
    RealPoint ccfCoordinates = new RealPoint(3);
    ccfCoordinates.setPosition([
        detection.getROI().getCentroidX(),
        detection.getROI().getCentroidY(),
        0
    ] as double[]);
    pixelToCCFTransform.apply(ccfCoordinates, ccfCoordinates);
    MeasurementList ml = detection.getMeasurementList();
    ml.addMeasurement("Allen CCFv3 X mm", ccfCoordinates.getDoublePosition(0) )
    ml.addMeasurement("Allen CCFv3 Y mm", ccfCoordinates.getDoublePosition(1) )
    ml.addMeasurement("Allen CCFv3 Z mm", ccfCoordinates.getDoublePosition(2) )

    if (!ml.containsNamedMeasurement("Subcellular: Channel 5: Num single spots")) {
        throw new Exception("Subcellular spot detection incomplete in this file. Please rerun subcellular spot detection on $imageName.")
    }

    ml.addMeasurement("Esr1 (Opal 480): Num Spots", ml.getMeasurementValue("Subcellular: Channel 2: Num single spots") )
    ml.addMeasurement("Prg (Opal 520): Num Spots", ml.getMeasurementValue("Subcellular: Channel 3: Num single spots") )
    ml.addMeasurement("Prlr (Opal 570): Num Spots", ml.getMeasurementValue("Subcellular: Channel 4: Num single spots") )
    ml.addMeasurement("Oxt (Opal 620): Num Spots", ml.getMeasurementValue("Subcellular: Channel 5: Num single spots") )
}}


// save annotations
File directory = new File(buildFilePath(PROJECT_BASE_DIR,'export'));
directory.mkdirs();
def filename = imageName.take(imageName.indexOf('.'))

saveMeasurements(
    imageData,
    PathCellObject.class,
    buildFilePath(directory.toString(),filename + '.tsv'),
    "Class", 
    "Allen CCFv3 X mm",
    "Allen CCFv3 Y mm",
    "Allen CCFv3 Z mm",
    "Esr1 (Opal 480): Num Spots",
    "Prg (Opal 520): Num Spots",
    "Prlr (Opal 570): Num Spots",
    "Oxt (Opal 620): Num Spots",
);
