require Net::RawIP;
use strict;

my $src = $ARGV[0];
my $dst = $ARGV[1];
my $file = $ARGV[2];
my $src_port=11111;
my $dst_port=514;

open FILE, "< $file";
while(my $line = <FILE>) {
  my $text = $line;
my $raw_packet = new Net::RawIP({'ip'=>{saddr=>$src, daddr=>$dst},'udp'=>{source=>$src_port, dest=>$dst_port, data=>$text}});

$raw_packet->send();}