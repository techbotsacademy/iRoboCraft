<script>
    let port;
    let writer;
    
    async function connectSerial() {
      port = await navigator.serial.requestPort();
      await port.open({ baudRate: 9600 });
      writer = port.writable.getWriter();
    }
    
    async function sendToArduino(text) {
      const encoder = new TextEncoder();
      await writer.write(encoder.encode(text + "\n"));
    }
</script>
