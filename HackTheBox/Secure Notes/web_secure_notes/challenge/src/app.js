const express = require('express');
const mongoose = require('mongoose');

const port = process.env.PORT ?? 3000;
const app = express();

const main = async () => {
    try {
        const uri = 'mongodb://localhost:27017/app';
        await mongoose.connect(uri);
        app.listen(port, () => {
            console.debug(`Server started on port ${port}`);
        });
    } catch (error) {
        console.error(error);
        process.exit(1);
    }
};

const Note = mongoose.model('Note', new mongoose.Schema({
    title: String,
    content: String,
}));

app.use(express.static('public'));
app.use(express.json());

app.get('/flag', (req, res) => {
    const remoteAddress = req.connection.remoteAddress;
    if (remoteAddress === '127.0.0.1' || remoteAddress === '::1' || remoteAddress === '::ffff:127.0.0.1') {
        res.send(process.env.FLAG ?? 'HTB{f4k3_fl4g_f0r_t3st1ng}');
    } else {
        res.status(403).json({ Message: 'Access denied' });
    }
});

app.post('/create', async (req, res) => {
    try {
        const { title, content } = req.body;
        if (typeof title !== 'string' || typeof content !== 'string') {
            res.status(400).json({ Message: 'Invalid title or content' });
            return;
        }
        const note = new Note({
            title,
            content,
        });
        await note.save();
        res.json(note);
    } catch (error) {
        console.error(error);
        res.status(500).json({ Message: "An error occurred" });
    }
});

app.get('/get/:noteId', async (req, res) => {
    try {
        const noteId = req.params.noteId;
        let note = await Note.findOne({ _id: noteId });
        res.json(note);
    } catch (error) {
        console.error(error);
        res.status(500).json({ Message: "An error occurred" });
    }
});

app.post('/update', async (req, res) => {
    try {
        const { noteId } = req.body;
        await Note.findByIdAndUpdate(noteId, req.body);
        let result = await Note.find({ _id: noteId });
        res.json(result);
    } catch (error) {
        console.error(error);
        res.status(500).json({ Message: "An error occurred" });
    }
});

main();