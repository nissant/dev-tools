# AT Cheat Sheet
A no frills AT usage document that reduces user frustration.
## Running AT
Run AT from the project's running folder where sim_conf.txt or at_conf.txt are located:
```
$ cd C:/projects/GW1/AT-RUN-PALLADIUM
```
Or:
```
$ cd C:/projects/GW1/AT-ASIC
```
Then:
```
$ python ../../gitlab/AT/AT/AT.py
```
## Setting Up at_conf.txt or sim_conf.txt
| Switch  											| Description 	|
| ------------- 									| ------------- |
| noloads  											| TBD  			|
| online  											| TBD  			|
| cli  												| TBD  			|
| sim												| TBD 			|
| dbg=dbg											| TBD 			|
| palladium											| TBD 			|
| oif=mipi											| TBD 			|
| noload											| TBD 			|
| reset=none										| TBD 			|
| streamer											| TBD 			|
| test_mode											| TBD 			|
| repo=C:\Projects\GW1\REPO\EVT0_1\Palladium\		| TBD 			|
| debug_events=.*ERROR.+							| TBD 			|
| image_quality_mode=SimpleIsp						| TBD 			|

## Load Setfile and Regsmap
```
> regsmap C:\work\GW1\REPO\ASIC\EVT0_1\GW1_MCD_EVT0_1_SVN#22409\RegMaps\GW1_EVT0_1.RegsMap_FW#14302.bin
> loads --setfile=C:\work\GW1\REPO\ASIC\EVT0_1\GW1_MCD_EVT0_1_SVN#22409\Setfiles\Setfiles_with_TNP\GW1MCD_EVT0_1_30fps_bin2_4fd_4624x3468_TcF_DPHY2388M_#4.tset
> loads --setfile=C:\work\GW1\REPO\ASIC\EVT0_1\GW1_MCD_EVT0_1_SVN#22409\Setfiles\Setfiles_with_TNP\GW1MCD_EVT0_1_13fps_nobin_Full_9248x6936_TcF_DPHY2388M_#1.tset
> loads --setfile=C:\work\GW2\REPO\ASIC\EVT0_1\GW2XX_EVT0_192Mclk_30fps_8K_CPHY2480.tset
> loads --setfile=C:\work\GW2\REPO\ASIC\EVT0_1\GW2XX_EVT0_192Mclk_214fps_4MP_2320x1736_CPHY2480.tset
> loads --setfile=C:\work\GW2\REPO\ASIC\EVT0\Operational\MIPI\GW2XX\DPHY1500\GW2XX_EVT0_120fps_bin4_BayerCF_FHD_DPHY1500_Modified.tset
```

## AT CLI
| Command  											| Description 	|
| ------------- 									| ------------- |
| TBD  												| TBD  			|
| TBD  												| TBD			|	
| TBD  												| TBD  			|
| TBD  												| TBD  			|

## Run XML Test
```
> test xml LSC_hardcoded.xml --repo=..\Repo\tests --mode=(30,3,NonaCF_12MP_wdr_3D_12024x9024)
> test xml RealImageInject.xml --repo=..\Repo\tests --mode=(21,0,TetraCF_64MP_9280x6944)
> test xml TCLSC_hardcoded.xml --repo=..\Repo\tests --mode=(21,0,TetraCF_64MP_9280x6944) --keepres
> test xml RealImageInject.xml --repo=..\Repo\tests --mode=(21,0,TetraCF_64MP_9280x6944_for_image_sanity_test)
> test xml bench_dark_IQC.xml --repo=..\Repo\tests --keepres --dbres
> test xml dark_IQC_hardcoded.xml --repo=..\Repo\tests --keepres --mode=(60,0,4_tap_elg_mode_1_X_Chip)
> test xml light_IQC_hardcoded.xml --repo=..\Repo\tests --keepres --mode=(60,0,4_tap_elg_mode_1_X_Chip)
> test xml bench_light_IQC_test.xml --repo=..\Repo\tests --keepres --dbres
> test xml bench_wdr_ratio_IQC.xml --repo=..\Repo\tests --keepres --dbres
> test xml bench_LCL_HCL_CR_hardcoded.xml --repo=..\Repo\tests --keepres
> test xml bench_SHBN_OECF.xml --repo=..\Repo\tests --keepres
```