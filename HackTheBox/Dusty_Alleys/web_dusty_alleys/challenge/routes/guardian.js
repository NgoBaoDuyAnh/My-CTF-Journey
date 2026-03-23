const node_fetch = require("node-fetch");
const router = require("express").Router();

router.get("/alley", async (_, res) => {
  res.render("index");
});

router.get("/think", async (req, res) => {
  return res.json(req.headers);
});

router.get("/guardian", async (req, res) => {
  const quote = req.query.quote;

  if (!quote) return res.render("guardian");

  try {
    const location = new URL(quote);
    const direction = location.hostname;
    if (!direction.endsWith("localhost") && direction !== "localhost")
      return res.send("guardian", {
        error: "You are forbidden from talking with me.",
      });
  } catch (error) {
    return res.render("guardian", { error: "My brain circuits are mad." });
  }

  try {
    let result = await node_fetch(quote, {
      method: "GET",
      headers: { Key: process.env.FLAG || "HTB{REDACTED}" },
    }).then((res) => res.text());

    res.set("Content-Type", "text/plain");

    res.send(result);
  } catch (e) {
    console.error(e);
    return res.render("guardian", {
      error: "The words are lost in my circuits",
    });
  }
});

module.exports = router;
