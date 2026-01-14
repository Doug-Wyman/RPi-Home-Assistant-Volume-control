<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<HEAD>
	<META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=windows-1252">
	<META NAME="GENERATOR" CONTENT="OpenOffice 4.1.5  (Win32)">
	<META NAME="CREATED" CONTENT="0;0">
	<META NAME="CHANGEDBY" CONTENT="Douglas Wyman">
	<META NAME="CHANGED" CONTENT="20260113;17085383">
</HEAD>
<BODY LANG="en-US" TEXT="#ffffff" BGCOLOR="#000000" DIR="LTR">
<H1 ALIGN=CENTER>MQTT Alsa Volume control for Home Assistant</H1>
<P ALIGN=CENTER>Updated Jan 14, 2026</P>
<H3 ALIGN=CENTER>"Requires python3-alsaaudio, use apt to install.</H3>
<P ALIGN=CENTER>If your Home Assistant uses the MQTT Integration,
this is a program <BR>to make a discover-able  MQTT remote control of
Alsa volume on a Raspberry Pi.<BR>n the Raspberry Pi, the Python
program runs at boot.<BR> 
It is initiated by systemd and runs as the desktop
user so it has access to the Alsa Mixer.<BR>The MQTT discovery packet
creates an instance of a &ldquo;light&rdquo; entity with a brightness
of 0 to 100. <A HREF="https://www.home-assistant.io/">Home Assistant</A></P>

<H1 ALIGN=CENTER>Installation</H1>
<P ALIGN=CENTER>Create a folder where you want the program to reside.</P>
<P ALIGN=CENTER>Copy the three files ( rpi_vol_control.py,
rpi-volume.service.template and setup.py)<BR>Make that your current
directory and run the python setup.py.<BR>Setup will prompt you for a
username, a unique entity name for Home Assistant,<BR>the IP address
or your MQTT broker and the location of the files. (filled in)<BR>The
app must  run as the desktop user so it can see the ALSA
controls..<BR>Setup creates a service file in /etc/systemd/system.<BR>It
executes, &ldquo;sudo systemctl daemon-reload&rdquo; to refresy
systemctl<BR>It executes, &ldquo;sudo systemctl enable
rpi-volume.service&rdquo; enabling the service<BR>Finally it
executes, &ldquo;sudo systemctl start rpi-volume.service&rdquo; to
start the service<BR>
</P>
<H1 ALIGN=CENTER>Homeassistant</H1>
<P ALIGN=CENTER>Bring up the homeassistant settings and look for the
unique name you used.<BR>The MQTT discovery in homeassistant should have found
and created the entity.
</P>
<H1 ALIGN=CENTER>Notes:</H1>
<P ALIGN=CENTER>Suggestions branches or anything to improve this is
welcome.</P>
</BODY>

</HTML>

