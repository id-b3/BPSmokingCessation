#!/usr/bin/awk -f

BEGIN {
    FS=","
}

# Expand the columns to _0-8
NR==1 {
    for(i=1;i<=NF;i++) {
        for(j=0;j<=8;j++) {
            printf "%s_%d%s", $i, j, (j==8 && i==NF? ORS: FS)
        }
    }
}

NR>1 {
    for(f=1;f<=NF;f++) {
        split($f,a,";");
        for(i=1; i<=9; i++){
            if(i <= length(a))
                printf a[i]
            printf (i==9 && f==NF ? ORS : FS)
        }
    }
}
