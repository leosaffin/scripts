!/home/zq822358/programming/ppvi/PVItoolbox

module pv_inversion

implicit none

contains

  subroutine balnc(fco, aps, ac, h, s, qe, tha, pe, part, thrs, maxx, maxxt,    &
                   omegs, omegh, nx, ny, nl)
  ! Calculates geopotential height and streamfunction by inverting an
  ! input pv field using the charney (1955) balance equation.

  !f2py      integer, intent(hide)    :: nx, ny, nl
  !f2py      real, intent(in)         :: fco(nx,ny)
  !f2py      real, intent(in)         :: aps(nx,ny)
  !f2py      real, intent(in)         :: ac(ny,5)
  !f2py      real, intent(inout)     :: h(nx,ny,nl)
  !f2py      real, intent(inout)     :: s(nx,ny,nl)
  !f2py      real, intent(inout)     :: qe(nx,ny,nl)
  !f2py      real, intent(inout)     :: tha(nx,ny,2)
  !f2py      real, intent(in)         :: pe(nl)
  !f2py      real, intent(in)         :: part
  !f2py      real, intent(in)         :: thrs
  !f2py      integer, intent(in)      :: maxx
  !f2py      integer, intent(in)      :: maxxt
  !f2py      real, intent(in)         :: omegs
  !f2py      real, intent(in)         :: omegh

  !-Input variables-------------------------------------------------------------
  ! Grid dimensions
  integer, intent(in) :: nx, ny, nl

  ! coriolis parameter
  real, intent(in) :: fco(nx,ny)

  ! ap ! cos(latitude)
  real, intent(in) :: aps(nx,ny)
      
  ! a  ! coefficients for 2-d laplacian operator
  real, intent(in) :: ac(ny,5)

  ! hz ! geopotential height
  real, intent(inout) :: h(nx,ny,nl)

  ! si ! streamfunction
  real, intent(inout) :: s(nx,ny,nl)

  ! q  ! pv (/0.01 pvu)
  real, intent(inout) :: qe(nx,ny,nl)

  ! tha(i,j,m)= boundary theta
  !    m=1 is lower boundary (midway between k=1    and k=2)
  !    m=2 is upper boundary (midway between k=nl-1 and k=nl)
  real, intent(inout) :: tha(nx,ny,2)

  ! pi ! exner function
  real, intent(in) :: pe(nl)

  ! prt ! relaxation parameter
  real, intent(in) :: part

  ! thr ! threshold parameter
  real, intent(in) :: thrs

  ! max ! maximum iterations
  real, intent(in) :: maxx

  ! maxt ! maximum cycles
  real, intent(in) :: maxxt

  ! omegas ! relaxation parameter for 2-d poisson equation
  real, intent(in) :: omegs

  ! omegah ! relaxation parameter for 3-d poisson equation
  real, intent(in) :: omegh

  !-Local variables-------------------------------------------------------------
      real :: mi,zm,rh(ny,nx,nl),zpl(ny,nx),zpp(ny),rs,gpts,            &
     &        stb(ny,nx,nl),asi(ny,nx,nl),bb(nl),bh(nl),bl(nl),         &
     &        vor,old(ny,nx,nl),dpi2(nl),nlco(ny,nx),coef(ny,nl),       &
     &        dh(ny,nx,nl),znl,rhs(ny,nx,nl),delh(ny,nx,nl),            &
     &        dsi(ny,nx,nl),vozro(nl),spzro(nl),maxhz(nl),              &
     &        minvor(nl),maxvor(nl),                                    &
     &        betas,dhmax,rha,rhst,sxx,sxy,syy,                         &
     &        zhl,zhp,zmrs,zl,zsl,zsp,zp

      integer :: i,J,K,igtz,ihm,iitot,iltz,insq,                        &
     &           itc,itc1,itcm,itcold,itct,jhm,khm

      logical :: it,icon

!-----------------------------------------------------------------------!
!                          start of subroutine                          !
!-----------------------------------------------------------------------!
      mi=9999.90
      gpts=float(ny*nx*(nl-2))

      iltz=0
      igtz=0
      insq=0
      itct=0
      itc1=0
      itc=0
      iitot=0
      itcold=0

      do k=1,nl
        vozro(k)=0.
        minvor(k)=100000.
        maxvor(k)=-100000.
      end do

      do i=2,ny-1
        zpp(i)=1./16.
        do  j=2,nx-1
          zpl(i,j)=1./(16.*aps(i,j)*aps(i,j))
          nlco(i,j)=2./( aps(i,j)*aps(i,j) )
        end do
      end do

      do k=1,nl
        bb(k)=0.
        bh(k)=0.
        bl(k)=0.
      end do

      do k=2,nl-1
        bb(k)=-2./( (pe(k+1)-pe(k))*(pe(k)-pe(k-1)) )
        bh(k)=2./( (pe(k+1)-pe(k))*(pe(k+1)-pe(k-1)) )
        bl(k)=2./( (pe(k)-pe(k-1))*(pe(k+1)-pe(k-1)) )
        dpi2(k)=(pe(k+1) - pe(k-1))/2.
        do i=1,ny
          coef(i,k)=ac(i,3)/bb(k)
        end do
      end do

      do k=1,nl
        maxhz(k)=0
      end do

      do k=1,nl
        do j=1,nx
          do i=1,ny
            old(i,j,k)=h(i,j,k)
            if (h(i,j,k)>maxhz(k)) then
              maxhz(k)=h(i,j,k)
            end if
          end do
        end do
      end do
!-----------------------------------------------------------------------!

  900 continue
      if (iitot == 0) go to 700
      itcm=0
      itc1=0
      do k=1,nl
        spzro(k)=0.
      end do

      do k=2,nl-1
        do j=2,nx-1
          do i=2,ny-1
            old(i,j,k)=s(i,j,k)
            if (k == 2) then
              old(i,j,1)=s(i,j,1)
            else if (k == nl-1) then
              old(i,j,nl)=s(i,j,nl)
            end if
            delh(i,j,k)= ac(i,1)*h(i-1,j,k) + ac(i,2)*h(i,j-1,k) +      &
     &                   ac(i,3)*h(i,j,k)   + ac(i,4)*h(i,j+1,k) +      &
     &                   ac(i,5)*h(i+1,j,k)

            stb(i,j,k)=bl(k)*h(i,j,k-1) + bh(k)*h(i,j,k+1) +            &
     &                 bb(k)*h(i,j,k)

            if (stb(i,j,k) <= 0.0001) then
              stb(i,j,k)=0.0001
               
!     modify boundary theta (k=2) or pv if static stability
!     becomes too small. theta becomes smaller; pv becomes larger
!     by a small amount (0.2 nondimensionally, which works out to
!     be perhaps a tenth of a degree K.
               
              if (k == 2) then
                tha(i,j,1)=tha(i,j,1)-0.2
              end if
              qe(i,j,k)=qe(i,j,k) + 0.2/(pe(k)-pe(k+1))
              spzro(k)=spzro(k) + 1
            end if
            sxx=s(i,j+1,k) + s(i,j-1,k) - 2.*s(i,j,k)
            syy=s(i-1,j,k) + s(i+1,j,k) - 2.*s(i,j,k)
            sxy=( s(i-1,j+1,k) - s(i-1,j-1,k) -                         &
     &            s(i+1,j+1,k) + s(i+1,j-1,k)  )/4.
            betas=0.25*((fco(i-1,j)-fco(i+1,j))*                        &
     &                  (s(i-1,j,k)-s(i+1,j,k)) +                       & 
     &                  (fco(i,j+1)-fco(i,j-1))*                        &
     &                  (s(i,j+1,k)-s(i,j-1,k)) )
            zhp=h(i-1,j,k+1)-h(i+1,j,k+1)-h(i-1,j,k-1)+h(i+1,j,k-1)
            zhl=h(i,j+1,k+1)-h(i,j-1,k+1)-h(i,j+1,k-1)+h(i,j-1,k-1)
            zsp=s(i-1,j,k+1)-s(i+1,j,k+1)-s(i-1,j,k-1)+s(i+1,j,k-1)
            zsl=s(i,j+1,k+1)-s(i,j-1,k+1)-s(i,j+1,k-1)+s(i,j-1,k-1)
            zl=zpl(i,j)*zhl*zsl/(dpi2(k)*dpi2(k))
            zp=zpp(i)*zhp*zsp/(dpi2(k)*dpi2(k))
            znl=nlco(i,j)*( sxx*syy - sxy*sxy ) + betas
            rhst = qe(i,j,k) - fco(i,j)*stb(i,j,k) + delh(i,j,k) -      &
     &             znl + zl + zp
            rhs(i,j,k)=rhst/(fco(i,j) + stb(i,j,k))

          end do
        end do
      end do

  23  format(f6.0,' neg stabilities.')
      do k=1,nl
        spzro(k)=0.
      end do

!*************iteration for psi **********************
      do k=2,nl-1
        itc=0
  800   continue
        it=.true.
        do j=2,nx-1
          do i=2,ny-1
            rs = ac(i,1)*s(i-1,j,k) + ac(i,2)*s(i,j-1,k) +              &
     &           ac(i,3)*s(i,j,k)   + ac(i,4)*s(i,j+1,k) +              &
     &           ac(i,5)*s(i+1,j,k) - rhs(i,j,k)
            dsi(i,j,k)=-omegs*rs/ac(i,3)
            s(i,j,k) = s(i,j,k) + dsi(i,j,k)
!*******check accuracy criterion *******************************
            if (abs(dsi(i,j,k)) > thrs) then
              it=.false.
            end if
          end do
        end do
      
        itc=itc+1
        if (it) then
          icon=.true.
          if (itc > itcm) itcm=itc
          if (itc == 1) itc1=itc1 + 1
        else
          if (itc < maxx) then
            go to 800
          else
            icon=.true.
          end if
        end if
      end do

      if (iitot > 0) then
        itct=itct + itcm
        do k=1,nl
          do j=2,nx-1
            do i=2,ny-1
              s(i,j,k)=part*s(i,j,k) + (1.-part)*old(i,j,k)
              old(i,j,k)=h(i,j,k)
            end do
          end do
        end do
      end if

!*************calculate the rhs of bal-pv eQuation (phi,h) ************

  700 continue
      do k=2,nl-1
        do j=2,nx-1
          do i=2,ny-1
            vor = ac(i,1)*s(i-1,j,k) + ac(i,2)*s(i,j-1,k) +             &
     &            ac(i,3)*s(i,j,k)   + ac(i,4)*s(i,j+1,k) +             &
     &            ac(i,5)*s(i+1,j,k)
            if (vor <= minvor(k)) then
              minvor(k)=vor
            end if
            if (vor >= maxvor(k)) then
              maxvor(k)=vor
            end if
            if (vor <= 0.0001-fco(i,j)) then
              vor = (0.0001 - fco(i,j))
!     increase pv where absolute vorticity is too small. similar to
!     case where stratification is too small.
              qe(i,j,k)=qe(i,j,k) + 0.01
              vozro(k)=vozro(k) + 1
            end if
            asi(i,j,k)=fco(i,j) + vor
            sxx=s(i,j+1,k)+s(i,j-1,k)-2.*s(i,j,k)
            syy=s(i-1,j,k)+s(i+1,j,k)-2.*s(i,j,k)
            sxy=( s(i-1,j+1,k) - s(i-1,j-1,k) -                         &
     &            s(i+1,j+1,k) + s(i+1,j-1,k)  )/4.
            zhp=h(i-1,j,k+1)-h(i+1,j,k+1)-h(i-1,j,k-1)+h(i+1,j,k-1)
            zhl=h(i,j+1,k+1)-h(i,j-1,k+1)-h(i,j+1,k-1)+h(i,j-1,k-1)
            zsp=s(i-1,j,k+1)-s(i+1,j,k+1)-s(i-1,j,k-1)+s(i+1,j,k-1)
            zsl=s(i,j+1,k+1)-s(i,j-1,k+1)-s(i,j+1,k-1)+s(i,j-1,k-1)
            zl=zpl(i,j)*zhl*zsl/(dpi2(k)*dpi2(k))
            zp=zpp(i)*zhp*zsp/(dpi2(k)*dpi2(k))
            betas=0.25*(                                                &
     &                  ( fco(i-1,j) - fco(i+1,j) )*                    &
     &                  ( s(i-1,j,k) - s(i+1,j,k) ) +                   & 
     &                  ( fco(i,j+1) - fco(i,j-1) )*                    &
     &                  ( s(i,j+1,k) - s(i,j-1,k) ) )
            rha=fco(i,j)*vor + nlco(i,j)*(sxx*syy - sxy*sxy) + betas
            rh(i,j,k)=rha + qe(i,j,k) + zl + zp
               
          end do
        end do
      end do

  24  format(i11,2f11.3,f6.0,' neg abs vorticities in phi eQ.')
      do k=1,nl
        vozro(k)=0.
      end do

!*************solve for h at each level *****************

      itc=0
  701 it=.true.
      zmrs=0.
      do k=2,nl-1
        do j=2,nx-1
          do i=2,ny-1
            if (k == 2) then
              rs = ac(i,1)*h(i-1,j,k) +                                 &
     &             ac(i,2)*h(i,j-1,k) +                                 &
     &            (ac(i,3) + asi(i,j,k)*(bb(k)+bl(k)) )*h(i,j,k) +      &
     &             ac(i,4)*h(i,j+1,k) +                                 & 
     &             ac(i,5)*h(i+1,j,k) +                                 &
     &             asi(i,j,k)*(bh(k)*h(i,j,k+1) +                       &
     &             tha(i,j,1)/dpi2(k)) - rh(i,j,k)
              zm = h(i,j,k)
              h(i,j,k) = zm - omegh*rs/(ac(i,3) +                       &
     &                                  asi(i,j,k)*(bb(k)+bl(k)))
               
            else if (k == nl-1) then
              rs = ac(i,1)*h(i-1,j,k) +                                 & 
     &             ac(i,2)*h(i,j-1,k) +                                 &
     &            (ac(i,3) + asi(i,j,k)*(bb(k)+bh(k)) )*h(i,j,k) +      &
     &             ac(i,4)*h(i,j+1,k) +                                 &
     &             ac(i,5)*h(i+1,j,k) +                                 &
     &             asi(i,j,k)*(bl(k)*h(i,j,k-1) -                       &
     &             tha(i,j,2)/dpi2(k)) - rh(i,j,k)
              zm = h(i,j,k)
              h(i,j,k) = zm - omegh*rs/(ac(i,3) +                       &
     &                                  asi(i,j,k)*(bb(k)+bh(k)))
               
            else
              rs = ac(i,1)*h(i-1,j,k) +                                 &
     &             ac(i,2)*h(i,j-1,k) +                                 &
     &            (ac(i,3) + asi(i,j,k)*bb(k) )*h(i,j,k) +              &
     &             ac(i,4)*h(i,j+1,k) +                                 &
     &             ac(i,5)*h(i+1,j,k) +                                 &
     &             asi(i,j,k)*( bh(k)*h(i,j,k+1) +                      &
     &                          bl(k)*h(i,j,k-1) ) -                    &
     &             rh(i,j,k)
              zm = h(i,j,k)
              h(i,j,k) = zm - omegh*rs/(ac(i,3) +                       &
     &                                  asi(i,j,k)*bb(k))
            end if
            dh(i,j,k)=h(i,j,k) - zm
            zmrs=zmrs + abs(dh(i,j,k))
            if (abs(dh(i,j,k)) > thrs) then
              it=.false.
            end if

          end do
        end do
      end do

      if (amod(float(itc),5.) == 0) then
        dhmax=thrs/10.
        zmrs=zmrs/gpts
        do k=2,nl-1
          do j=2,nx-1
            do i=2,ny-1
              if (abs(dh(i,j,k)) > dhmax) then
                dhmax=abs(dh(i,j,k))
                ihm=i
                jhm=j
                khm=k
              end if
            end do
          end do
        end do

  716   format(2e9.2,3i5,f8.3)
      end if
      zmrs=0.

      itc=itc+1
      if (it) then
        itct=itct + itc
        do j=1,nx
          do i=1,ny
            h(i,j,1) = h(i,j,2) + tha(i,j,1)*(pe(2)-pe(1))
            s(i,j,1) = s(i,j,2) + tha(i,j,1)*(pe(2)-pe(1))
            h(i,j,nl) = h(i,j,nl-1) - tha(i,j,2)*(pe(nl)-pe(nl-1))
            s(i,j,nl) = s(i,j,nl-1) - tha(i,j,2)*(pe(nl)-pe(nl-1))
          end do
        end do
         
        if (iitot > 0) then
          do k=1,nl
            do j=2,nx-1
              do i=2,ny-1
                h(i,j,k)=part*h(i,j,k) + (1.-part)*old(i,j,k)
              end do
            end do
          end do
        end if
        if ( (itc > itcold+10).and.(iitot > 30) ) then
          print*,'started diverging'
          go to 901
        end if
        itcold=itc
        if ((itc == 1).and.(itc1 == nl-2)) then
          print*,'total convergence.'
        else
          iitot=iitot + 1
  22      format(i4,' total iteration(s).')
          if (iitot > maxxt) then
            print*,'too many total iterations.'
            go to 901
          else
            go to 900
          end if
        end if
      else
        if (itc < maxx) then
          go to 701
        else
          print*,'too many iterations for hght.'
          icon=.false.
          go to 901
        end if
      end if
!*******************************************************
 901  return
      end subroutine balnc

end module pv_inversion
