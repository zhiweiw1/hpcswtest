$-----------------------------------------------------------------------------
$
$ Example provided by Iñaki (LSTC)
$
$ E-Mail: info@dynamore.de
$ Web: http://www.dynamore.de
$
$ Copyright, 2015 DYNAmore GmbH
$ Copying for non-commercial usage allowed if
$ copy bears this notice completely.
$
$X------------------------------------------------------------------------------
$X
$X 1. Run file as is.
$X    Requires LS-DYNA MPP R8.0.0 (or higher) with double precision 
$X
$X------------------------------------------------------------------------------
$# UNITS: Dimensionless. 
$X------------------------------------------------------------------------------
$X
*KEYWORD
*TITLE
ICFD Cylinder flow
*INCLUDE
mesh.k
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
$                                                                              $
$                             PARAMETERS                                       $
$                                                                              $
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
*PARAMETER
R    T_end     100.0
R  dt_plot      1.00
$
$--- Fluid
$
R  v_inlet       1.0
Rrho_fluid       1.0
R mu_fluid     0.005 
R dt_fluid     0.000
$
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
$                                                                              $
$                           ICFD CONTROL CARDS                                 $
$                                                                              $
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
*ICFD_CONTROL_TIME
$#     ttm        dt
    &T_end &dt_fluid
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
$                                                                              $
$                       ICFD PARTS/ SECTION/ MATERIAL                          $
$                                                                              $
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
*ICFD_SECTION
$#     sid   
         1
*ICFD_MAT
$#     mid       flg        ro       vis          
         1         1&rho_fluid &mu_fluid       
*ICFD_PART
$#     pid     secid       mid 
         1         1         1
*ICFD_PART
$#     pid     secid       mid 
         2         1         1
*ICFD_PART
$#     pid     secid       mid 
         3         1         1
*ICFD_PART
$#     pid     secid       mid 
         4         1         1
*ICFD_PART_VOL
$#     pid     secid       mid 
        10         1         1
$#   spid1     spid2     spid3     spid4
         1         2         3         4
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
$                                                                              $
$                    ICFD BOUNDARY/INITIAL CONDITIONS                          $
$                                                                              $
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
*ICFD_BOUNDARY_PRESCRIBED_VEL
$#     pid       dof       vad      lcid       
         1         1         1         1      
*ICFD_BOUNDARY_PRESCRIBED_VEL
$#     pid       dof       vad      lcid       
         1         2         1         2       
*ICFD_BOUNDARY_PRESCRIBED_PRE
$#     pid      lcid        sf     death     birth     
         2         2     
*ICFD_BOUNDARY_FREESLIP
$#     pid   
         3
*ICFD_BOUNDARY_NONSLIP
$#     pid   
         4
*DEFINE_CURVE_TITLE
Velocity inlet
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp
         1                    &v_inlet
$#                a1                  o1
                 0.0                 1.0
             10000.0                 1.0
*DEFINE_CURVE_TITLE
Pressure outlet
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp
         2
$#                a1                  o1
                 0.0                 0.0
             10000.0                 0.0
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
$                                                                              $
$                            ICFD MESH KEYWORDS                                $
$                                                                              $
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
*MESH_VOLUME
$#   volid     
         1
$#    pid1      pid2      pid3      pid4     
         1         2         3         4     
*MESH_BL
$#     pid     nelth
         4         2
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
$                                                                              $
$                             DATABASE (OUTPUT)                                $
$                                                                              $
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
*ICFD_DATABASE_DRAG
$#     pid
         4
*DATABASE_BINARY_D3PLOT
&dt_plot
*END