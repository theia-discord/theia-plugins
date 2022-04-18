#!/usr/bin/env bash

while read -r line
do
    if [ "x$(echo "$line" | jq -r '.CommandInvoke.cmd.command')" == "xecho" ]
    then
        output="$(echo "$line" | jq '.CommandInvoke.cmd | .start_flags + .arguments + .end_flags | map_values(tostring) | join(" ")')"
        channel="$(echo "$line" | jq '.CommandInvoke.message.channel_id')"
        reply_to="$(echo "$line" | jq '.CommandInvoke.message.message_id')"

        printf '{"SendMessage":{"channel_id":%s,"in_reply_to":%s,"content":%s}}\n' "$channel" "$reply_to" "$output"
    fi
done
