tell application "Messages"
	set targetService to service "SMS"
	set targetBuddy to buddy "RNUMBER" of targetService
	send "RMESSAGE" to targetBuddy
end tell
