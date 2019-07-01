# Creating the Chair/Stool Classifier a la code

## Getting Up And Running

The system requirements are the same as **part 1**.  You're going to need to be running MacOS Catalina 10.15 in order to work with most of these new APIs, most notably, `MLImageClassifier`.

Go ahead and open up a new, **Blank**, playground.

Remove everything except the first line and import CreateML.  Your playground should look like this before we get moving:

```
import Cocoa
import CreateML
```

## Preparing Your Data

We're working with the same dataset as in **part 1** of this series, so head there to do the setup if you haven't already.  Or, have a look at the official documentation [here](https://developer.apple.com/documentation/createml/creating_an_image_classifier_model) under "Prepare Your Data".

Putting your data in this structure is going to allow us to harness the power of `MLImageClassifier.DataSource` which automatically interprets your class names and training data by the folder structure.  Simply provide a URL to your training data set and you're ready to rock.

```
/*
  Get the URL of the directory that holds your data. 
  Mine is on my desktop. Change the location as necessary.
*/
let desktopURL = FileManager.default.urls(for: .desktopDirectory, 
                                          in: .userDomainMask).first
guard let url = desktopURL else { 
    fatalError("Can't find Downloads directory")
}

// Get the URL to my specific training data set, which contains the folders 'Chair' and 'Stool'
let trainingDataURL = desktopURL.appendingPathComponent("Dataset/train")`
```
Next, pass the training data URL to the `MLImageClassifier.DataSource.labeledDirectories` constructor which will use the folder names as the labels for the training data, just as it does in the Create ML UI.

`let dataSource = MLImageClassifier.DataSource.labeledDirectories(at: trainingDataURL)`

## Training The Model

Modern ML tools have abstracted model training to the point where it can mostly be done with a single line of code, as is in the case of CreateML.

```
// Training begins immediately when this line is run
let classifierV1 = try MLImageClassifier(trainingData: dataSource)
```
And we're done!  Really.  With our small data set and CreateML's powerful feature extractor (explained in a bit) your model should be nearly done by the time you've finished reading this.

### Parameter Customization

You could call it a day on training at this point, but let's look at how you might tweak some of your parameters that will be used in training your classifier.

By default, Create ML will configure the following parameters for you:
* scenePrint v1 feature extractor
* 25 max iterations
* auto validation (10%?) - This is my guess based on console print-outs when using 'auto'
* No augmentation options

You can tweak these by instantiating your own `ModelParameters` struct.

```
// Leaving `validationData` as `nil` will default to auto
let parameters = MLImageClassifier.ModelParameters(featureExtractor: .scenePrint(revision: 1),
                                                   validationData: nil,
                                                   maxIterations: 20,
                                                   augmentationOptions: [.crop])
```

Let's discuss...

#### Feature Extractor

In CreateML, you're not actually training a complete model with all the trimmings. The Feature Extractor allows you to map your output to a much more sophisticated pre-trained model in the OS in a process know as transfer learning, resulting in fewer images needed for training and a smaller final model size.
 
 [Learn more in the docs](https://developer.apple.com/documentation/createml/mlimageclassifier/modelparameters/3006548-featureextractor)
 
#### Scene Print

Scene print is the name of the default feature extractor already trained on millions of real world images. (Note: it is not meant for character recognition).

While using scene print is easily the fastest route to highly accurate models, CreateML also allows you to provide your own custom base models to work with the feature extractor.
 
 [Learn more in the docs](https://developer.apple.com/documentation/createml/mlimageclassifier/featureextractortype/sceneprint_revision)

#### Augmentation

Augmentation is a process that automatically creates additonal training data out of your exsiting samples.  Options include crop, rotation, blur, exposure, noise, and flip.  Augmentations can also compound with one another, resulting in up to a limit of 100 new variations of each image.  This is extrememly helpful in buidling a more robust model when you have a limited dataset.
 
 [Learn more in the docs](https://developer.apple.com/documentation/createml/mlimageclassifier/imageaugmentationoptions)

Now that we've exhausted a basically discussion of parameter customization, here's how you'd build the same classifier when providing those parameters.

`let classifierV2 = try MLImageClassifier(trainingData: dataSource, parameters: parameters)`

### Unorganized Data

What if you're images aren't in the specified order required for using a `MLImageClassifier.DataSource`?

Easy.  First, get the directories where your training data is located.
```
let chairTrainingURL = trainingDataURL.appendingPathComponent("Chair")
let stoolTrainingURL = trainingDataURL.appendingPathComponent("Stool")
```

Next, you'll want the urls of the images in those directories in an array like so:

```
// Note that the image names don't matter, call them whatever you'd like.
let mockURLs = [
    chairTrainURL.appendingPathComponent("chair123.jpg"),
    chairTrainURL.appendingPathComponent("seatXYZ.jpg")
]
```

However, I wrote a quick extension to easily get the individual URLs within a given directory so I don't need to provide all the image names individually.
```
extension FileManager {
    func urls(for url: URL, skipsHiddenFiles: Bool = true ) -> [URL]? {
        let fileURLs = try? contentsOfDirectory(at: url, includingPropertiesForKeys: nil, options: skipsHiddenFiles ? .skipsHiddenFiles : [] )
        return fileURLs
    }
}
```

Use the extension like so to create a dictionary in the format of `[className : urlsForClassImages]:`
```
let chairTrainingURLs = FileManager.default.urls(for: chairTrainingURL) ?? []
let stoolTrainURLs = FileManager.default.urls(for: stoolTrainingURL) ?? []

let trainingData = ["Chair": chairTrainingURLs, "Stool": stoolTrainingURLs]
```

Now we're ready to provide our data from a custom location as well as our custom parameters from before.
```
let classifierV3 = try MLImageClassifier(trainingData: trainingData,
                                       parameters: parameters)
```

When your training is off and running, you can expect something like the print out below to show up in your console.  

```
4 augmented images by 'crop' to be generated.
Automatically generating validation set from 10% of the data.
Extracting augmented image features from training data set.
Analyzing and extracting image features.
+----------------------+------------------+--------------+------------------+
| Raw Images Processed | Augmented Images | Elapsed Time | Percent Complete |
+----------------------+------------------+--------------+------------------+
VPA info: plugin is INTEL, AVD_id = 1080020, AVD_api.Create:0x107a5bdec
| 1                    | 5                | 2.14s        | 2.25%            |
| 2                    | 10               | 2.41s        | 4.5%             |
| 3                    | 15               | 2.68s        | 6.75%            |
| 4                    | 20               | 2.96s        | 9%               |
| 5                    | 25               | 3.23s        | 11.25%           |
| 10                   | 50               | 4.63s        | 22.5%            |
| 25                   | 125              | 8.81s        | 56.75%           |
| 44                   | 220              | 14.03s       | 100%             |
| 43                   | 215              | 13.74s       | 97.5%            |
+----------------------+------------------+--------------+------------------+
```

Here we see slightly more information than we can see in CreateML UI such as the number of additional augmented images for each original image.
 

## Inspecting The Classifier

### Training

We can find out a little bit more about our classifier by calling a few new APIs. `trainingMetrics` gives us info about the data our classifier was trained on.
```
classifierV3.trainingMetrics

// Number of examples: 220
// Number of classes: 2
// Accuracy 100.00%
```

### Validation

Likewise, `validationMetrics` mimic those metric.  Keep in mind that since our training set was so small, our validation set was only a couple of images plus there augmented versions, hence, why the accuracy number is so low.
```
classifierV3.validationMetrics

// Number of examples: 6
// Number of classes: 2
// Accuracy 66.67%
```

### Model Description

Some information about the resulting model we created:

```
classifierV3.model.modelDescription

MLModelDescription: MLModelDescription inputDescriptionsByName: {
    image = "image : Image (Color, 299 x 299)";
} outputDescriptionsByName: {
    classLabel = "classLabel : String";
    classLabelProbs = "classLabelProbs : Dictionary (String \U2192 Double)";
} predictedFeatureName: classLabel predictedProbabilitiesName: classLabelProbs metadata: {
    MLModelAuthorKey = "";
    MLModelCreatorDefinedKey =     {
    };
    MLModelDescriptionKey = "";
    MLModelLicenseKey = "";
    MLModelVersionStringKey = "";
}
```
A few interesting things to note:

#### Input Type

Our input type is `image : Image (Color, 299 x 299)`
* If you provide training images less than 299x299 they will be scaled up and could reduce accuracy
* Try to provide training images that will be simliar to the types of images you'll predict against in your app.  i.e. If you'll be predicting foods in a grocery store, use training data from indoor photos that might represent that type of enviornment.

#### Output Type

Our classifier outputs two details for us:
* The class name in String format.  i.e "Chair"
* A dictionary of each class and it's associated confidence.  i.e. `["Chair" : 0.99, "Stool" : 0.01]`

#### Metadata

You'll notice currently our model is missing metadata such as author, license, etc.  We'll correct this later when we export our model.

### Classifier Description

Here we essentially see a combination of the training and validation metrics in a single output.
```
classifierV3.description

// ImageClassifier
 
// Parameters
// Feature Extractor: ScenePrint
// Max Iterations: 20
 
// Performance on Training Data
// Number of examples: 220
// Number of classes: 2
// Accuracy: 100.00%
 
// Performance on Validation Data
// Number of examples: 6
// Number of classes: 2
// Accuracy: 66.67%
```
 
The debug description is even more thorough and includes the confusion matrix.
```
classifierV3.debugDescription

// ImageClassifier
// ----------------------------------
// Feature Extractor: ScenePrint
// Max Iterations: 20
 
// Performance on Training Data
// ----------------------------------
// Number of examples: 220
// Number of classes: 2
// Accuracy: 100.00%
 
// ******CONFUSION MATRIX******
// ----------------------------------
// True\Pred Chair  Stool
// Chair     110    0
// Stool     0      110
 
// ******PRECISION RECALL******
// ----------------------------------
// Class Precision(%)   Recall(%)
// Chair 100.00         100.00
// Stool 100.00         100.00
 
// Performance on Validation Data
// ----------------------------------
// Number of examples: 6
// Number of classes: 2
// Accuracy: 66.67%
 
// ******CONFUSION MATRIX******
// ----------------------------------
// True\Pred Chair  Stool
// Chair     3      0
// Stool     2      1
 
// ******PRECISION RECALL******
// ----------------------------------
// Class Precision(%)   Recall(%)
// Chair 60.00          100.00
// Stool 100.00         33.33
```
### Confusion Matrix

If you're new to ML, you're probably asking what this is.  It's a bit out of scope for this post, but I'll give you two quick examples that are commonly used as explanation for these concepts:

#### Accuracy

If your model predicts 98 out of 100 test examples correctly, your accuracy is 98%.  Simple.  But accuracy may not always the best measure of performance for your use case.

#### Recall (DO get it right)

Out of all people that receive cancer screenings, it's a pretty low chance that one will actually have cancer.  Therefore you could create a model that always predicts 'no-cancer' and probably still get a 99.9% accurate model.  But you'd also be missing the 0.01% of people who actually have cancer, missing the point despite the high accuracy.  

Better would be a model that elimates all false negatives.  Meaning for every 'no-cancer' prediction you make, you better be 100% right.  It's better to incorrectly predict that someone has cancer when they actually don't so that they can receive further testing right away.  You cast a wider net to capture all cancer cases.

#### Precision (DON'T get it wrong)

On the opposite end, if you had a model that consequently sent people to jail if found guilty, you would want to ensure you eliminated all false positives.  It's better to give up accuracy in order to ensure you don't send an innocent person to jail.

### Evaluation 

You can supply your testing data either by using the same `dataSource` we created earlier, or by following the same procedure of creating a `[className : urlsForClassImages]` that points to your test images.

```
let metrics = classifierV3.evaluation(on: dataSource)

// Number of examples: 50
// Number of classes: 2
// Accuracy 88.00%
```

For the small dataset we used, I'm pretty pleased with the accuracy here.  We could obviously increase the accuracy by providing many more training images than we did.

Let's grab a single sample and check out how our classifier performs:

```
let chairTestURLs = FileManager.default.urls(for: chairTrainURL) ?? []

guard let randomChair = chairTestURLs.randomElement(), let prediction = try? classifierV3.prediction(from: randomChair) else {
    fatalError("Could not get prediction for element")
}

//88% chance it'll show 'Chair' ;) 
prediction 
```

My only call out here is that `classifierV3.prediction(from: randomChair)` returns only a `String` and not a struct or some format that would include the confidence as well as the class name.  Using the Create ML UI you would also be shown the confidence.

Additionally, when utilizing your model in an actual app, you'll get a confidence score along with your prediciton (as the model description output above promised).

### Metadata And Export

Almost done!  Let's prepare some metadata to be added to our model before exporting.
```
let metadata = MLModelMetadata(author: "MLGuru",
                               shortDescription: "Chair/Stool classifier",
                               license: nil,
                               version: "1.0",
                               additional: ["Truth?" : "Indeed"])
```
The `additional` parameter per the docs is described as: 
> A dictionary that encodes key value pairs to hold additional information about the model.

But honestly, I could not see where this information appeared when viewing the final exported model in XCode.

Let's export this model already:

```
// Set the location
let dataURL = desktopURL.appendingPathComponent("Dataset")

// And export!  
try? classifierV3.write(to: dataURL.appendingPathComponent("ChairClassifier.mlmodel"), metadata: metadata)
```

### Ready To Serve

Open your resulting model in XCode and inspect.

![](https://i.imgur.com/Yk6uYmf.png)

17 KB!  Checkout the discussion above on Feature Extraction on how this impressive number is achieved.  

Lastly, drag and drop any test image into the 'Experimentation' section of the UI and you'll recieve the class and confidence as a result.

![](https://i.imgur.com/tnPbARN.png)

## Conclusion

It's always interesting to dig under the hood of Apple's black box tooling.  As someone who also works regularly with Python and Notebooks to explore machine learning, creating our classifier in code feels more fluid to me than in the UI.

Further, if we were to improve upon our Playground we could essentially use it as a script to create future models.  We could provide additional functionality to split a data set into training and testing folders, assign class names, etc.

Ultimately, while the CreateML UI is a powerful tool to get moving quickly with ML, if you know a little bit of Swift, it's probably worth your time to punch out a few lines in your Playground if you'll be using it more than once.

But either way you choose, CreateML is a wonderful tool for easing developers into the machine learning world and offer them a quick way to create new models for their applications.