#!/usr/bin/perl
use strict;
use warnings;
use Math::Trig;
use 5.010;

my @params;
our $pi = pi;

open my $param_f, "<", "./param" or die "Can't open param:$!\n";
while(my $line = <$param_f>)
{
    chomp($line);
    if($line =~ /^\.param.*\=\s*(.*)/)
    {
        push @params, $1;
    }
    else
    {
        say "Invalid line in param:$line";
    }
}
close $param_f;

`shekel @params > result.po`;

# open my $xxfh, ">", "xx";
# say $xxfh "@params";
# close $xxfh;
# `matlab -nojvm < ./shekel.m`;

sub cosine
{
    die "Dim shoule be 2\n" if not(scalar @_ == 2);
    my($x, $y) = @_;
    my $u      = 1.6 * $x - 0.5;
    my $v      = 1.6 * $y - 0.5;
    return 1 - ($u**2 + $v**2 - 0.3 * cos(3 * $pi * $u) - 0.3 * cos(3 * $pi * $v));
}

sub rosenbrock
{
    die "Dim shoule be 2\n" if not(scalar @_ == 2);
    my($x, $y) = @_;
    return 10 - 100 * ($y - $x**2)**2 - (1.0 - $x)**2;
}

sub michal
{
    my @xs  = @_;
    my $m   = 10;
    my $sum = 0.0;
    for my $idx (1..scalar @xs)
    {
        my $xi = $xs[$idx-1];
        $sum += sin($xi) * sin($idx * $xi**2 / $pi)**(2*$m);
    }
    return $sum;
}

sub brainin
{
    my @xs    = @_;
    my $x1    = $xs[0];
    my $x2    = $xs[1];
    my $t     = 1 / (8*$pi);
    my $s     = 10;
    my $r     = 6;
    my $c     = 5/$pi;
    my $b     = 5.1 / (4*$pi**2);
    my $a     = 1;
    my $term1 = $a * ($x2 - $b*$x1**2 + $c*$x1 - $r)**2;
    my $term2 = $s*(1-$t)*cos($x1);
    my $y     = $term1 + $term2 + $s;
    return $y - 0.397887;
}

sub shekel
{
    my @xs = @_;

    my $ret = `./shekel @xs`;
    return $ret;

    # open my $xx_fh, ">", "xx" or die "Can't create xx:$!\n";
    # say $xx_fh "@xs";
    # `matlab -nojvm < shekelMf.m`;

    # open my $rfh, "<", "shekel_ret" or die "Can't open shekel_ret:$!\n";
    # chomp(my $ret = <$rfh>);
    # close $rfh;
    # return $ret;
}
