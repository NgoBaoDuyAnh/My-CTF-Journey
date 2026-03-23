const express = require("express");
const path = require("path")
const app = express();
const guardian = require("./routes/guardian");
const PORT = process.env.PORT || 1337;


app.set("view engine", "ejs");
app.set("views", path.join(process.cwd(), "views"));
app.use(express.static('public'));
app.use(guardian);

app.listen(PORT, () => {
  console.log(`Server Running on ${PORT}`);
});
