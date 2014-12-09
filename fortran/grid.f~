! Subroutine volume
! Calculates the volume of grid boxes give the dimensions
! Computed using a spherical integral
      SUBROUTINE volume(rho,bounds,theta,phi,nz,ny,nx,boxes)

      IMPLICIT NONE

      INTEGER nz,ny,nx
              ! Grid Dimensions
      REAL    rho(nz,ny,nx),                                            &
              ! Height (Earth Radius + Altitude)
     &        bounds(nz,ny,nx,2),                                       &
              ! Height at edges of each gridbox
     &        theta(nx),                                                &
              ! Longitude
     &        phi(ny),                                                  &
              ! 90 - Latitude
     &        boxes(nz,ny,nx)
              ! Volume of grid boxes

CF2PY      INTEGER, INTENT(HIDE)    :: nz
CF2PY      INTEGER, INTENT(HIDE)    :: ny
CF2PY      INTEGER, INTENT(HIDE)    :: nx
CF2PY      REAL, INTENT(IN)         :: rho(nz,ny,nx)
CF2PY      REAL, INTENT(IN)         :: bounds(nz,ny,nx,2)
CF2PY      REAL, INTENT(IN)         :: theta(nx)
CF2PY      REAL, INTENT(IN)         :: phi(ny)
CF2PY      REAL, INTENT(OUT)        :: boxes(nz,ny,nx)

!     Local Variables
      REAL :: dtheta,dphi
      INTEGER :: i,j,k

!-----------------------------------------------------------------------!
!                          START OF SUBROUTINE                          !
!-----------------------------------------------------------------------!
      dtheta = theta(2) - theta(1)
      dphi = phi(2) - phi(1)
      DO k=1,nz
        DO j=1,ny
          DO i=1,nx
            boxes(k,j,i) = ABS(rho(k,j,i)**2 * sin(phi(j)) *            &
     &                         (bounds(k,j,i,2) - bounds(k,j,i,1)) *    &
     &                         dtheta * dphi)
          END DO
        END DO
      END DO

      END SUBROUTINE volume
