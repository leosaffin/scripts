! Subroutine volume
! Calculates the volume of grid boxes give the dimensions
! Computed using a spherical integral
      SUBROUTINE VOLUME(rho,bounds,theta,phi,nz,ny,nx,boxes)

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

      END SUBROUTINE VOLUME

! Subroutine GRAD
! Calculates the magnitude of the vector gradient in spherical polar
! coordinates
! Gradients using centred ~2nd order differences
      SUBROUTINE GRAD(field,rho,theta,phi,nz,ny,nx,output)

      IMPLICIT NONE

      INTEGER nz,ny,nx
              ! Grid Dimensions
      REAL    field(nz,ny,nx),                                          &
              ! Values of input field
     &        rho(nz,ny,nx),                                            &
              ! Height (Earth Radius + Altitude)
     &        theta(nx),                                                &
              ! Longitude
     &        phi(ny),                                                  &
              ! 90 - Latitude
     &        output(nz,ny,nx)
              ! Magnitude of the vector gradient

CF2PY      INTEGER, INTENT(HIDE)    :: nz
CF2PY      INTEGER, INTENT(HIDE)    :: ny
CF2PY      INTEGER, INTENT(HIDE)    :: nx
CF2PY      REAL, INTENT(IN)         :: rho(nz,ny,nx)
CF2PY      REAL, INTENT(IN)         :: theta(nx)
CF2PY      REAL, INTENT(IN)         :: phi(ny)
CF2PY      REAL, INTENT(OUT)        :: output(nz,ny,nx)

!     Local Variables
      REAL :: d_dR(nz,ny,nx), d_dTheta(nz,ny,nx), d_dPhi(nz,ny,nx)
      INTEGER :: i,j,k

!-----------------------------------------------------------------------!
!                          START OF SUBROUTINE                          !
!-----------------------------------------------------------------------!

! Calculate Vertical Component
      DO k=2,nz-1
        DO j=1,ny
          DO i=1,nx
            d_dR(k,j,i) = (field(k+1,j,i) - field(k-1,j,i))/            &
     &                    (  rho(k+1,j,i) -   rho(k-1,j,i))
          END DO
        END DO
      END DO

! Calculate Longitudinal Component
      DO k=1,nz
        DO j=1,ny
          DO i=2,nx-1
            d_dTheta(k,j,i) = (1/(rho(k,j,i)*SIN(phi(j)))) *            &
     &                         (((field(k,j,i+1) - field(k,j,i-1))/     &
     &                           (    theta(i+1) - theta(i-1)   )))
          END DO
        END DO
      END DO

! Calculate Latitudinal Component
      DO k=1,nz
        DO j=2,ny-1
          DO i=1,nx
            d_dPhi(k,j,i) = (1/rho(k,j,i))*                               &
     &                       (((field(k,j+1,i) - field(k,j-1,i))/       &
     &                         (      phi(j+1) - phi(j-1)     )))
          END DO
        END DO
      END DO

! Calculate Vector Gradient Magnitude
      DO k=1,nz
        DO j=1,ny
          DO i=1,nx
            output(k,j,i) = SQRT(d_dr(k,j,i)**2 +                       &
     &                           d_dTheta(k,j,i)**2 +                   &
     &                           d_dPhi(k,j,i)**2)
          END DO
        END DO
      END DO

      END SUBROUTINE GRAD
