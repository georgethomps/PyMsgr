tell application "Messages"
	set targetService to 1st service whose service type = iMessage
	set targetBuddy to buddy "RNUMBER" of targetService
	send "RMESSAGE" to targetBuddy
end tell