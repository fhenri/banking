const multer = require("multer");

const BAK_FOLDER = "./tmp/bank-uploads";
// Create the multer instance
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    // This part defines where the files need to be saved
    cb(null, BAK_FOLDER);
  },
  filename: (req, file, cb) => {
    // This part sets the file name of the file
    cb(null, `${Date.now()}-${file.originalname}`);
  },
});

// Then we will set the storage
const multipart = multer({ storage: storage });

//const destFolder = "uploads/";
//const multipart = multer({ dest: BAK_FOLDER });

module.exports = multipart;
