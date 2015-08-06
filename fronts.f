!-----------------------------------------------------------------------!
!                          Grad 2D                                      !
!-----------------------------------------------------------------------!
      subroutine grad2d(x, dx, nx, ny, grad)

      implicit none

      integer ny, nx
              ! Grid Dimensions
      real    x(ny, nx),                                                 &
              ! 2d array
     &        dx,                                                        &

     &        grad(ny, nx, 2)

CF2PY integer, intent(hide) :: nx
CF2PY integer, intent(hide) :: ny
CF2PY real, intent(in) :: dx
CF2PY real, intent(in) :: x(ny, nx)
CF2PY real, intent(out) :: grad(ny, nx, 2)

      ! Local Variables
      integer :: i,j
!-----------------------------------------------------------------------!
!                          START OF SUBROUTINE                          !
!-----------------------------------------------------------------------!
      grad = 0.0
      do j=2,ny-1
        do i=2,nx-1
          grad(j, i, 1) = (x(j, i+1) - x(j, i-1)) / (2*dx)
          grad(j, i, 2) = (x(j+1, i) - x(j-1, i)) / (2*dx)
        end do
      end do

      end subroutine grad2d

!-----------------------------------------------------------------------!
!                          Div 2D                                       !
!-----------------------------------------------------------------------!
      subroutine div2d(beta, D, dx, nx, ny, div)

      implicit none

      integer ny, nx
              ! Grid Dimensions
      real    beta(ny, nx), D(ny, nx),                                   &
     &        dx,                                                        &
     &        div(ny, nx)

CF2PY integer, intent(hide) :: nx
CF2PY integer, intent(hide) :: ny
CF2PY real, intent(in) :: beta(ny, nx)
CF2PY real, intent(in) :: D(ny, nx)
CF2PY real, intent(in) :: dx
CF2PY real, intent(in) :: x(ny, nx)
CF2PY real, intent(out) :: div(ny, nx)

      ! Local Variables
      integer :: i,j
      real :: d1, d2, d3, d4
!-----------------------------------------------------------------------!
!                          START OF SUBROUTINE                          !
!-----------------------------------------------------------------------!
      div = 0.0
      do j=2,ny-1
        do i=2,nx-1
          d1 = D(j-1,i)*(cos(beta(j-1,i))*cos(beta(j,i)) +               &
     &                   sin(beta(j-1,i))*sin(beta(j,i)))

          d2 = D(j,i-1)*(cos(beta(j,i-1))*cos(beta(j,i)) +               &
     &                   sin(beta(j,i-1))*sin(beta(j,i)))

          d3 = D(j,i+1)*(cos(beta(j,i+1))*cos(beta(j,i)) +               &
     &                   sin(beta(j,i+1))*sin(beta(j,i)))

          d4 = D(j+1,i)*(cos(beta(j+1,i))*cos(beta(j,i)) +               &
     &                   sin(beta(j+1,i))*sin(beta(j,i)))

          div(j,i) = (d4 - d1 + d3 - d2)/2*dx
        end do
      end do

      end subroutine div2d

!-----------------------------------------------------------------------!
!                          5 Point Ave                                  !
!-----------------------------------------------------------------------!
      subroutine fivepointave(x, dx, nx, ny, ave)

      implicit none

      integer ny, nx
              ! Grid Dimensions
      real    x(ny, nx),                                                 &
              ! 2d array
     &        dx,                                                        &

     &        ave(ny, nx)

CF2PY integer, intent(hide) :: nx
CF2PY integer, intent(hide) :: ny
CF2PY real, intent(in) :: dx
CF2PY real, intent(in) :: x(ny, nx)
CF2PY real, intent(out) :: ave(ny, nx)

      ! Local Variables
      integer :: i,j
!-----------------------------------------------------------------------!
!                          START OF SUBROUTINE                          !
!-----------------------------------------------------------------------!
      ave = 0.0
      do j=2,ny-1
        do i=2,nx-1
          ave(j, i) = 0.2*(x(j-1,i)+x(j,i-1)+x(j,i)+x(j,i+1)+x(j+1,i))
        end do
      end do

      end subroutine fivepointave

!-----------------------------------------------------------------------!
!                          Mean Axis                                    !
!-----------------------------------------------------------------------!
      subroutine mean_axis(x, dx, nx, ny, means)

      implicit none

      integer ny, nx
              ! Grid Dimensions
      real    x(ny, nx, 2),                                              &
              ! 2d array
     &        dx,                                                        &

     &        means(2,ny,nx)

CF2PY integer, intent(hide) :: nx
CF2PY integer, intent(hide) :: ny
CF2PY real, intent(in) :: dx
CF2PY real, intent(in) :: x(ny, nx, 2)
CF2PY real, intent(out) :: means(2, ny, nx)

      ! Local Variables
      integer :: i,j
      real :: beta, D, Dcos2beta(ny,nx), Dsin2beta(ny,nx), P, Q
!-----------------------------------------------------------------------!
!                          START OF SUBROUTINE                          !
!-----------------------------------------------------------------------!
      do j=1,ny
        do i=1,nx
          beta = atan2(x(j,i,2), x(j,i,1))
          D = sqrt(x(j,i,1)**2 + x(j,i,2)**2)
          Dcos2beta(j,i) = D*cos(2*beta)
          Dsin2beta(j,i) = D*sin(2*beta)
        end do
      end do

      means=0.0
      do j=2,ny-1
        do i=2,nx-1
          P = Dcos2beta(j-1,i) + Dcos2beta(j,i-1) + Dcos2beta(j,i) +      &
     &        Dcos2beta(j,i+1) + Dcos2beta(j+1,i)
          Q = Dsin2beta(j-1,i) + Dsin2beta(j,i-1) + Dsin2beta(j,i) +      &
     &        Dsin2beta(j,i+1) + Dsin2beta(j+1,i)
          means(1,j,i) = 0.5 * atan2(Q, P)
          means(2,j,i) = 0.2 * sqrt(P**2 + Q**2)
        end do
      end do

      end subroutine mean_axis
