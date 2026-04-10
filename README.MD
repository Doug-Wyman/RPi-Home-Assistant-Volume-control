<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<HEAD>
	<META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=windows-1252">
	<TITLE></TITLE>
	<META NAME="GENERATOR" CONTENT="OpenOffice 4.1.5  (Win32)">
	<META NAME="CREATED" CONTENT="0;0">
	<META NAME="CHANGEDBY" CONTENT="Douglas Wyman">
	<META NAME="CHANGED" CONTENT="20260410;14412163">
	<META NAME="CHANGEDBY" CONTENT="Douglas Wyman">
	<STYLE TYPE="text/css">
	<!--
		H1 { color: #ffffff }
		P { color: #ffffff }
		H3 { color: #ffffff }
		H3.cjk { font-family: "SimSun" }
		H3.ctl { font-family: "Lucida Sans" }
	-->
	</STYLE>
</HEAD>
<BODY LANG="en-US" TEXT="#ffffff" BGCOLOR="#000000" DIR="LTR">
<H1 ALIGN=CENTER>MQTT Alsa Volume control for Home Assistant</H1>
<P ALIGN=CENTER>Updated Apr 10, 2026</P>
<H3 CLASS="western" ALIGN=CENTER>&quot;Requires python3-alsaaudio,
use apt to install.</H3>
<P ALIGN=CENTER>If your Home Assistant uses the MQTT Integration,
this is a program <BR>to make a discover-able MQTT remote control of
Alsa volume on a Raspberry Pi.<BR>on the Raspberry Pi, the Python
program runs at boot.<BR>It is initiated by systemd and runs as the
desktop user so it has access to the Alsa Mixer.<BR>The MQTT
discovery packet creates an instance of a &ldquo;light&rdquo; entity
with a brightness of 0 to 100.  I have upgraded it to run on
Bookworm. <A HREF="https://www.home-assistant.io/">Home Assistant</A></br>
<H1 ALIGN=CENTER>Installation</H1>
<P ALIGN=CENTER>In your home folder create 2 folders. One will be for
Python virtual environments.</br>I named mine .venvs.  In that folder the various Home
assistant automation folders</br>reside.  For this volume control it will contain the
folder rpi-volume.  The second folder</br>is copied to the home folder.  The volume folder
contains the Python script and a copy</br>of the systemd service file, rpi-volume.service which
will reside in /etc/systemd.system.</br>The Python script will need to be edited to change
the MQTT broker address.</br>Copy the service file to /etc/systemd.system and run 
</br>&ldquo;sudo systemctl enable rpi-volume.service&rdquo;
 
</br>then &ldquo;sudo systemctl start rpi-volume.service&rdquo;</br>All of the needed python add-ons are in the virtual
environment</br>If python does not recognize the add-ons they may
have to be installed.</br>If so &ldquo;/.venvs/volume/pip install&rdquo; must
be used.</br> 
</P>
<H1 ALIGN=CENTER>Notes:</H1>
<P ALIGN=CENTER>Suggestions branches or anything to improve this is
welcome.</P>
</BODY>
</HTML>