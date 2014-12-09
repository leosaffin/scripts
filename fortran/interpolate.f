! Subroutine volume
! Calculates the volume of grid boxes give the dimensions
! Computed using a spherical integral
      SUBROUTINE any_to_pressure(field,pressure,prange,                 &
     &                           np,nz,ny,nx,newfield)

      IMPLICIT NONE

      INTEGER np,nz,ny,nx
              ! Grid Dimensions
      REAL    field(nz,ny,nx),                                          &
              ! Input Field
     &        pressure(nz,ny,nx)                                        &
              ! Pressure on same level as input field
     &        newfield(nz,ny,nx)
              ! Output field interpolated to pressure levels

CF2PY      INTEGER, INTENT(HIDE)    :: np
CF2PY      INTEGER, INTENT(HIDE)    :: nz
CF2PY      INTEGER, INTENT(HIDE)    :: ny
CF2PY      INTEGER, INTENT(HIDE)    :: nx
CF2PY      REAL, INTENT(IN)         :: field(nz,ny,nx)
CF2PY      REAL, INTENT(IN)         :: pressure(nz,ny,nx)
CF2PY      REAL, INTENT(IN)         :: prange(np)
CF2PY      REAL, INTENT(OUT)        :: newfield(np,ny,nx)

!     Local Variables
      REAL :: dtheta,dphi
      INTEGER :: i,j,k

!-----------------------------------------------------------------------!
!                          START OF SUBROUTINE                          !
!-----------------------------------------------------------------------!

      DO k=1,np
        DO j=1,ny
          DO i=1,nx
            IF (prange(k)<pressure(nz,j,i)) THEN
              newfield(l,j,i)
            boxes(k,j,i) = ABS(rho(k,j,i)**2 * sin(phi(j)) *            &
     &                         (bounds(k,j,i,2) - bounds(k,j,i,1)) *    &
     &                         dtheta * dphi)
          END DO
        END DO
      END DO

      END SUBROUTINE volume
