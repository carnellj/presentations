sudo apt-get --assume-yes install pulseaudio pulseaudio-module-bluetooth

#dpkg -l pulseaudio pulseaudio-module-bluetooth

echo -e 'pair 81:76:A5:2D:02:ED' | bluetoothctl
echo -e 'trust 81:76:A5:2D:02:ED' | bluetoothctl
echo -e 'connect 81:76:A5:2D:02:ED' | bluetoothctl

sudo killall bluealsa

pulseaudio --start

pacmd list-cards


pacmd set-card-profile bluez_card.81_76_A5_2D_02_ED a2dp_sink

pacmd set-default-sink bluez_sink.81_76_A5_2D_02_ED.a2dp_sink

sudo wget https://steady-holiday-6497.twil.io/assets/imperialmarch-5954.mp3 -P /Music/
