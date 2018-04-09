#!/usr/bin/env pythopc1

#A simple example for communicating with a Raspberry Pi from a browser. Uses the Bottle Python web framework, and jQuery AJAX.

from bottle import route, request, run, get
import socket
import time
import threading
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.output(11, True)

GPIO.setup(12, GPIO.OUT)
GPIO.output(12, True)

GPIO.setup(13, GPIO.OUT)
GPIO.output(13, True)

GPIO.setup(15, GPIO.OUT)
GPIO.output(15, True)

ip_address = ["192.168.1.16", "192.168.1.17", "192.168.1.15", "192.168.1.113"]
on = '<span id="on"> Online </span>'
off = '<span id="off"> Offline </span>'

lock = threading.Lock()
machines = {ip_address[0]:off, ip_address[1]:off, ip_address[2]:off, ip_address[3]:off} 

def pingSystem(host):
    while True:
        lock.acquire()
        response = os.system("ping -c 1 -W 5 " + host)
        if response == 0:
            machines[host] = on
        else:
            machines[host] = off
        lock.release()
        time.sleep(1)

@route('/power')
def power():
    return '''
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="http://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
<link rel="stylesheet" href="/resources/demos/style.css">
<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet"> 
<script src="http://code.jquery.com/jquery-1.10.2.min.js"</script>
<script src="http://code.jquery.com/mobile/1.4.2/jquery.mobile-1.4.2.min.js></script>
<script>

$(document).ready(function() {
  var pc0_is_off = 1;
  var pc1_is_off = 1;
  var pc2_is_off = 1;
  var pc3_is_off = 1;
  var pc0_force_off = 0;
  var pc1_force_off = 0;
  var pc2_force_off = 0;
  var pc3_force_off = 0;
    
  $(document).mouseup(function() {
    pc0_is_off = 1;
    pc0_force_off = 0;
    $.ajax({
            url: '/pc0',
            type: 'POST',
            data: { pc0:pc0_is_off, pc0_f:pc0_force_off }
    });
    
    pc1_is_off = 1;
    pc1_force_off = 0;
    $.ajax({
            url: '/pc1',
            type: 'POST',
            data: { pc1:pc1_is_off, pc1_f:pc1_force_off }
    });
    
    pc2_is_off = 1;
    pc2_force_off = 0;
    $.ajax({
            url: '/pc2',
            type: 'POST',
            data: { pc2:pc2_is_off, pc2_f:pc2_force_off }
    });
    
    pc3_is_off = 1;
    pc3_force_off = 0;
    $.ajax({
            url: '/pc3',
            type: 'POST',
            data: { pc3:pc3_is_off, pc3_f:pc3_force_off }
    });
  });
  
  $("#pc0, #pc0-force")
    .mousedown(function() {
        if(this.id == 'pc0') { 
            pc0_is_off = 0;
            pc0_force_off = 0;}
        else if(this.id == 'pc0-force') { pc0_force_off = 1; }
	else {
            pc0_is_off = 1;
	    pc0_force_off = 0; }   
    $.ajax({
            url: '/pc0',
            type: 'POST',
            data: { pc0:pc0_is_off, pc0_f:pc0_force_off }  
      });
    })

  $("#pc1, #pc1-force")
    .mousedown(function() {
        if(this.id == 'pc1') { 
            pc1_is_off = 0;
            pc1_force_off = 0;}
        else if(this.id == 'pc1-force') { pc1_force_off = 1; }    
        else {
            pc1_is_off = 1;
	    pc1_force_off = 0;}
    $.ajax({
            url: '/pc1',
            type: 'POST',
            data: { pc1:pc1_is_off, pc1_f:pc1_force_off }  
      });
    })
    
  $("#pc2, #pc2-force")
    .mousedown(function() {
        if(this.id == 'pc2') { 
            pc2_is_off = 0;
            pc2_force_off = 0;}
        else if(this.id == 'pc2-force') { pc2_force_off = 1; }    
        else {
            pc2_is_off = 1;
	    pc2_force_off = 0; }
     $.ajax({
            url: '/pc2',
            type: 'POST',
            data: { pc2:pc2_is_off, pc2_f:pc2_force_off }  
      });
    });

  $("#pc3, #pc3-force")
    .mousedown(function() {
        if(this.id == 'pc3') { 
            pc3_is_off = 0;
            pc3_force_off = 0;}
        else if(this.id == 'pc3-force') { pc3_force_off = 1; }    
        else {
            pc3_is_off = 1;
            pc3_force_off = 0; }
    $.ajax({
            url: '/pc3',
            type: 'POST',
            data: { pc3:pc3_is_off, pc3_f:pc3_force_off }  
      });
    });
});



</script>
<style>

body{
padding-top: 50px;
background-color: #ddd;
text-align: center;
}

h1 {
color: #16A61B
}

#on {
  color: white;
  background-color: #16A61B;
  padding: 10px;
}

#off {
  color: white;
  background-color: #C64545;
  padding: 10px;
}

</style>
</head>
<h1>Power Manager</h1>
<body style="font-family: 'Roboto', sans-serif;">
<div data-role="page">
 <p>Click power for 1:1 power button action. Click Force-off to initiate 5 second hold. Reload page for current on/off statuses (based on network connectivity).</p>
  <div data-role="main">
    <form>
        <p>
        PC1:
        <input type="button" class="ui-button ui-widget ui-corner-all" value="Power" data-role="button" id="pc0">
        <input type="button" class="ui-button ui-widget ui-corner-all" value="Force-off" data-role="button" id="pc0-force">
        ''' + machines[ip_address[0]] + '''
        </p> 

        <p>
        PC2:
        <input type="button" class="ui-button ui-widget ui-corner-all" value="Power" data-role="button" id="pc1">
        <input type="button" class="ui-button ui-widget ui-corner-all" value="Force-off" data-role="button" id="pc1-force">
        ''' + machines[ip_address[1]] + '''
        </p>
        <p>
        PC3:
        <input type="button" class="ui-button ui-widget ui-corner-all" value="Power" data-role="button" id="pc2">
        <input type="button" class="ui-button ui-widget ui-corner-all" value="Force-off" data-role="button" id="pc2-force">
        ''' + machines[ip_address[2]] + '''
        </p>
        <p>
        PC4:
        <input type="button" class="ui-button ui-widget ui-corner-all" value="Reset" data-role="button" id="pc3">
        <!--input type="button" class="ui-button ui-widget ui-corner-all" value="Force-off" data-role="button" id="pc3-force"-->
        ''' + machines[ip_address[3]] + '''
        </p>
    </form>
 </div>
</div>
</body>
</html>
'''

pc0_busy = 0
pc1_busy = 0
pc2_busy = 0
pc3_busy = 0

@route('/pc0', method='POST')
def pc0():
    global pc0_busy
    pc0_is_off = bool(int(request.forms.get('pc0')))
    pc0_f = bool(int(request.forms.get('pc0_f')))
    if pc0_f:
        pc0_busy = 1
        GPIO.output(11, False)
        time.sleep(5.5)
        GPIO.output(11, True)
        pc0_busy = 0
    elif not pc0_busy:
        GPIO.output(11, pc0_is_off)

@route('/pc1', method='POST')
def pc1():
    global pc1_busy
    pc1_is_off = bool(int(request.forms.get('pc1')))
    pc1_f = bool(int(request.forms.get('pc1_f')))
    if pc1_f:
        pc1_busy = 1
        GPIO.output(12, False)
        time.sleep(5.5)
        GPIO.output(12, True)
        pc1_busy = 0
    elif not pc1_busy:
        GPIO.output(12, pc1_is_off)

@route('/pc2', method='POST')
def pc2():
    global pc2_busy
    pc2_is_off = bool(int(request.forms.get('pc2')))
    pc2_f = bool(int(request.forms.get('pc2_f')))
    if pc2_f:
        pc2_busy = 1
        GPIO.output(13, False)
        time.sleep(5.5)
        GPIO.output(13, True)
        pc2_busy = 0
    elif not pc2_busy:
        GPIO.output(13, pc2_is_off)

@route('/pc3', method='POST')
def pc3():
    global pc3_busy
    pc3_is_off = bool(int(request.forms.get('pc3')))
    pc3_f = bool(int(request.forms.get('pc3_f')))
    if pc3_f:
        pc3_busy = 1
        GPIO.output(15, False)
        time.sleep(5.5)
        GPIO.output(15, True)
        pc3_busy = 0
    elif not pc3_busy:
        GPIO.output(15, pc3_is_off)

if __name__ == '__main__':

    pc0_thread = threading.Thread(target=pingSystem, args=[ip_address[0]])
    pc0_thread.daemon = True
    pc0_thread.start()

    pc1_thread = threading.Thread(target=pingSystem, args=[ip_address[1]])
    pc1_thread.daemon = True
    pc1_thread.start()

    pc2_thread = threading.Thread(target=pingSystem, args=[ip_address[2]])
    pc2_thread.daemon = True
    pc2_thread.start()
    
    pc3_thread = threading.Thread(target=pingSystem, args=[ip_address[3]])
    pc3_thread.daemon = True
    pc3_thread.start()
    
    while True: 
        try:
            run(host = '0.0.0.0', port = '8080', server='paste')
        except (socket.gaierror, socket.error, KeyboardInterrupt) as err:
            print("Error occurred: %s"%err)
            time.sleep(2)
