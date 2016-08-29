#!/usr/bin/perl

require './zfsmanager-lib.pl';
&ReadParse();

my %conf = get_zfsmanager_config();

ui_print_header(undef, $text{'index_title'}, '', undef, 1, 1, 0, &help_search_link('zfs, zpool', 'man', 'doc', 'google'), undef, undef, $text{'index_version'} );

# define tabs
@tabs = (
    [ 'pools', 'ZFS Pools', 'index.cgi?mode=pools' ],
    [ 'zfs', 'ZFS File Systems', 'index.cgi?mode=zfs' ],
  );
if ($conf{'list_snap'}) { push(@tabs, [ 'snapshot', 'Snapshots', 'index.cgi?mode=snapshot' ]); }

# start tabes
$in{'mode'} ||= 'pools';
print &ui_tabs_start(\@tabs, 'mode', $in{'mode'}, 1);

# start pools tab
print &ui_tabs_start_tab('mode', 'pools');
# must be in a form!
#if ($conf{'pool_properties'}) {
#  print "<a href='create.cgi?create=zpool'>Create new pool<a/>";
#  print ' | ';
#  print "<a href='create.cgi?import=1'>Import pool<a/>";
#}
my $zpool = list_zpools();
print_zpool('status.cgi?pool=',\%$zpool);
print &ui_tabs_end_tab();

# start zfs tab
print &ui_tabs_start_tab('mode', 'zfs');
my %zfs = list_zfs();
print_zfs('status.cgi?zfs=',\%zfs);
if ($conf{'zfs_properties'}) { print "<a href='create.cgi?create=zfs'>Create file system</a>"; }
print &ui_tabs_end_tab();

# start snapshots tab
if ($conf{'list_snap'}) {
  print &ui_tabs_start_tab('mode', 'snapshot');
  ui_snapshot_list(undef);
  if ($conf{'snap_properties'}) { print "<a href='create.cgi?create=snapshot'>Create snapshot</a>"; }
  print &ui_tabs_end_tab();
}

# end tabs
print &ui_tabs_end(1);

#alerts
print '<h3>Alerts: </h3>', get_alerts(), "";

ui_print_footer('/', $text{'index'});
