# KCM
KCM Classifies Music

King's Group K Sheet Music Classifier

## methodology
### data extraction
* Capture image of sheet music
* Find primary data (e.g. BPM, time signature)
* Remove stave lines and repair note breakages
* Flood fill to separate the notes
* Use logistic model to predict the note
* Sum values of frequency of notes, note length and primary data

