#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
use Data::Dumper;
%conf = get_zfsmanager_config();

#show pool status
if ($in{'pool'})
{
ui_print_header(undef, $text{'status_title'}, "", undef, 1, 1);

#Show pool information
#print "Pool:";
ui_zpool_status($in{'pool'});

#show properties for pool
ui_zpool_properties($in{'pool'});

#Show device configuration
my $root = "00000000";
my %status = zpool_status($in{'pool'});

#-- status table--
print ui_table_start("Status", "width=100%", "10");
print ui_table_row("Scan:", $status{$root}{scan});
print ui_table_row("Read:", $status{$root}{read});
print ui_table_row("Write:", $status{$root}{write});
print ui_table_row("Checkum:", $status{$root}{cksum});
print ui_table_row("Errors:", $status{$root}{errors});
print ui_table_end();

if ($status{$root}{status} or $status{$root}{action} or $status{pool}{see}) {
  print ui_table_start("Attention", "width=100%", "10");
  if ($status{$root}{status}) { print ui_table_row("Status:", $status{$root}{status}); }
  if ($status{$root}{action}) { print ui_table_row("Action:", $status{$root}{action}); }
  if ($status{$root}{see})    { print ui_table_row("See:",    $status{$root}{see}); }
  print ui_table_end();
}

#-- tasks table--
print ui_table_start("Tasks", "width=100%", "10", ['align=left'] );
#print ui_table_row("Snapshot: ", ui_create_snapshot($in{'zfs'}));
if ($conf{'zfs_properties'}) {
  print ui_table_row("New file system: ", "<a href='create.cgi?create=zfs&parent=$in{pool}'>Create file system</a>");
  #print ui_table_row('Export ',  "<a href='cmd.cgi?cmd=export&pool=$in{pool}'>Export pool</a>");
}
if ($conf{'pool_properties'}) {
  if ($status{$root}{scan} =~ /scrub in progress/) { print ui_table_row('Scrub ',"<a href='cmd.cgi?cmd=scrub&stop=y&pool=$in{pool}'>Stop scrub</a>"); }
  else { print ui_table_row('Scrub ', "<a href='cmd.cgi?cmd=scrub&pool=$in{pool}'>Scrub pool</a>");}
  print ui_table_row('Upgrade ', "<a href='cmd.cgi?cmd=upgrade&pool=$in{pool}'>Upgrade pool</a>");
  print ui_table_row('Export ',  "<a href='cmd.cgi?cmd=export&pool=$in{pool}'>Export pool</a>");
}
if ($conf{'pool_destroy'}) { print ui_table_row("Destroy ", "<a href='cmd.cgi?cmd=pooldestroy&pool=$in{pool}'>Destroy this pool</a>"); }
print ui_table_end();

#-- zfs table--
#Show associated file systems
%zfs = list_zfs("-r ".$in{'pool'});
print_zfs("status.cgi?zfs=",\%zfs);

#-- vdev table--
print ui_columns_start([ "Virtual Device", "State", "Read", "Write", "Cksum" ]);
foreach $key (sort keys %status)
{
	if (($status{$key}{parent} =~ /pool/) && ($key ne $root)) {
		print ui_columns_row(["<a href='config-vdev.cgi?pool=".$status{0}{pool}.'&dev='.$key."'>".$status{$key}{name}."</a>", $status{$key}{state}, $status{$key}{read}, $status{$key}{write}, $status{$key}{cksum}]);
	} elsif ($key ne $root) {
		print ui_columns_row(["<a href='config-vdev.cgi?pool=".$status{0}{pool}.'&dev='.$key."'>|_".$status{$key}{name}."</a>", $status{$key}{state}, $status{$key}{read}, $status{$key}{write}, $status{$key}{cksum}]);
	}
}
print ui_columns_end();

ui_print_footer('', $text{'index_return'});
}

#show filesystem status
if ($in{'zfs'})
{
	ui_print_header(undef, "ZFS File System", "", undef, 1, 1);
	#start tabs
	
	#@tabs = ();
	#push(@tabs, [ "status", "Status", "index.cgi?mode=status&zfs=$in{'zfs'}" ]);
	#push(@tabs, [ "edit", "Edit", "index.cgi?mode=edit&zfs=$in{'zfs'}" ]);
	#push(@tabs, [ "snapshot", "Snapshots", "index.cgi?mode=snapshot&zfs=$in{'zfs'}" ]);
	#print &ui_tabs_start(\@tabs, "mode", $in{'mode'} || $tabs[0]->[0], 1);

	#start status tab
	#print &ui_tabs_start_tab("mode", "status");
	#ui_zfs_list('-r '.$in{'zfs'});
	ui_zfs_list($in{'zfs'});

	#show properties for filesystem
	ui_zfs_properties($in{'zfs'});
	#print Dumper(\%ary)."<br />";

  #--tasks table--
  print ui_table_start("Tasks", "width=100%", "10");
  if ($conf{'snap_properties'}) { print ui_table_row("Snapshot: ", ui_create_snapshot($in{'zfs'})); }
  if ($conf{'zfs_properties'}) {
    #print ui_table_row("New file system: ", ui_popup_link('Create child file system', "create.cgi?create=zfs&parent=$in{'zfs'}"));
    print ui_table_row("New file system: ", "<a href='create.cgi?create=zfs&parent=".$in{'zfs'}."'>Create child file system</a>");
    if (index($in{'zfs'}, '/') != -1) { print ui_table_row("Rename: ", "<a href='create.cgi?rename=".$in{'zfs'}."'>Rename ".$in{'zfs'}."</a>"); }
    if ($hash{$in{'zfs'}}{origin}) { print ui_table_row("Promote: ", "This file system is a clone, <a href='cmd.cgi?cmd=promote&zfs=$in{zfs}'>promote $in{zfs}</a>"); }
  }
  if ($conf{'zfs_destroy'}) { print ui_table_row("Destroy: ", "<a href='cmd.cgi?cmd=zfsdestroy&zfs=$in{zfs}'>Destroy this file system</a>"); }
  print ui_table_end();
	
	#show list of snapshots based on filesystem
	#print "Snapshots on this filesystem: <br />";
	ui_list_snapshots('-rd1 '.$in{'zfs'});
	my %hash = zfs_get($in{'zfs'}, "all");
	
	ui_print_footer('index.cgi?mode=zfs', $text{'zfs_return'});
	
}

#show snapshot status
#show status of current snapshot
if ($in{'snap'})
{
	ui_print_header(undef, $text{'snapshot_title'}, "", undef, 1, 1);
	#print zfs_get($in{'snap'}, "all");
	%snapshot = list_snapshots($in{'snap'});
	print ui_columns_start([ "Snapshot", "Used", "Refer" ]);
	foreach $key (sort(keys %snapshot)) 
	{
		print ui_columns_row(["<a href='status.cgi?snap=$key'>$key</a>", $snapshot{$key}{used}, $snapshot{$key}{refer} ]);
	}
	print ui_columns_end();
	ui_zfs_properties($in{'snap'});

	#print "<a href='cmd.cgi?destroy=", $in{'snap'}, "'>Destroy snapshot</a> |";
	my $zfs = $in{'snap'};
	$zfs =~ s/\@.*//;
	
	#--tasks table--
	print ui_table_start('Tasks', 'width=100%', undef);
	print ui_table_row('Differences', "<a href='diff.cgi?snap=$in{snap}'>Show differences in $in{'snap'}</a>");
	if ($conf{'snap_properties'}) { 
		#print ui_table_row('Snapshot:', "<a href='snapshot.cgi?zfs=$zfs'>Create new snapshot based on $zfs</a>");
		print ui_table_row("Snapshot: ", ui_create_snapshot($zfs));
		#print ui_table_row('Rename:', "Rename $in{'snap'}");
		print ui_table_row("Rename: ", "<a href='create.cgi?rename=".$in{'snap'}."'>Rename ".$in{'snap'}."</a>");
	}
	if ($conf{'zfs_properties'}) { 
		print ui_table_row('Clone:', "<a href='create.cgi?clone=$in{snap}'>Clone $in{'snap'} to new file system</a>"); 
	}
	if ($conf{'snap_properties'} && $conf{'zfs_properties'}) { 
		#print ui_table_row('Clone:', "Clone $in{'snap'} to new file system"); 
		print ui_table_row('Rollback:', "Rollback $zfs to $in{'snap'}");
		#print ui_table_row('Send:', "Send $in{'snap'}");
	}
	if ($conf{'snap_destroy'}) { print ui_table_row('Destroy:',"<a href='cmd.cgi?cmd=snpdestroy&snapshot=$in{snap}'>Destroy snapshot</a>", ); }
	print ui_table_end();
	if ($conf{'list_snap'}) { ui_print_footer('index.cgi?mode=snapshot', $text{'snapshot_return'}); } else { ui_print_footer('index.cgi?mode=zfs', $text{'zfs_return'}); }
}

