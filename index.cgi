#!/usr/bin/perl

require './zfsmanager-lib.pl';
&ReadParse();
use Data::Dumper;
ui_print_header(undef, $text{'index_title'}, "", undef, 1, 1, 0, &help_search_link("zfs, zpool", "man", "doc", "google"), undef, undef, $text{'index_version'} );

my %conf = get_zfsmanager_config();

#start tabs
@tabs = ();
#push(@tabs, [ "pools", "ZFS Pools", "index.cgi?mode=pools" ]);
#push(@tabs, [ "zfs", "ZFS File Systems", "index.cgi?mode=zfs" ]);
#if ($conf{'list_snap'} =~ /1/) { push(@tabs, [ "snapshot", "Snapshots", "index.cgi?mode=snapshot" ]); }

push(@tabs, [ "pools", "ZFS Pools" ]);
push(@tabs, [ "zfs", "ZFS File Systems" ]);
if ($conf{'list_snap'} =~ /1/) { push(@tabs, [ "snapshot", "Snapshots" ]); }

print &ui_tabs_start(\@tabs, "mode", $in{'mode'} || $tabs[0]->[0], 1);

#start pools tab
print &ui_tabs_start_tab("mode", "pools");
%zpool = list_zpools();
print_zpool("status.cgi?pool=",\%zpool);
if ($conf{'pool_properties'} =~ /1/) { 
	print "<a href='create.cgi?create=zpool'>Create new pool<a/>";
	print " | ";
	print "<a href='create.cgi?import=1'>Import pool<a/>";
}
print &ui_tabs_end_tab("mode", "pools");

#start zfs tab
print &ui_tabs_start_tab("mode", "zfs");
%zfs = list_zfs();
print_zfs("status.cgi?zfs=",\%zfs);
if ($conf{'zfs_properties'} =~ /1/) { print "<a href='create.cgi?create=zfs'>Create file system</a>"; }
print &ui_tabs_end_tab("mode", "zfs");

#start snapshots tab
if ($conf{'list_snap'} =~ /1/) {
  print &ui_tabs_start_tab("mode", "snapshot");
  ui_list_snapshots(undef, 1);
  if ($conf{'snap_properties'} =~ /1/) { print "<a href='create.cgi?create=snapshot'>Create snapshot</a>"; }
  print &ui_tabs_end_tab("mode", "snapshot");
}

#end tabs
print &ui_tabs_end(1);

#alerts
print "<h3>Alerts: </h3>", get_alerts(), "";

ui_print_footer("/", $text{'index'});
