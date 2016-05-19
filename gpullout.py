import math
import matplotlib.pyplot as plt
import numpy as np

g = 9.81

ktToms = 0.5144444444
msTokt = 1.0 / ktToms
mToft = 3.2808399

def magnitude(x, y):
    return math.sqrt(x*x + y*y)

def ramp(startVal, endVal, period, time):
    if(time > period):
        return endVal
    return startVal + ((endVal - startVal) / period) * time

def IAStoTAS(ias, alt):
    return ias + ias * 0.02 * (alt/1000)

# Setup graph
fig = plt.figure(1, figsize=(8.5, 8.5))
ax = plt.subplot(111)
ax.yaxis.grid(True)
ax.xaxis.grid(True)
ax.set_ylim(-10000, 0)

start, end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(start, end, 1000))

Lg = 4.0 
Wg = 1.0
Dg = 0.1
Tg = 0.0

times = []
alts = []

def gPullOut(initialVelocity, initialFPA):
    t = 0
    dt = 0.1

    fpa = math.radians(initialFPA)

    Vx = initialVelocity * ktToms * math.cos(fpa)
    Vy = initialVelocity * ktToms * math.sin(fpa) * -1.0

    alt = 0

    times.clear()
    alts.clear()
    times.append(0)
    alts.append(0)

    # TEMP TODO
    #Lg = 1.0 * math.cos(fpa)

    while(fpa >= 0.0):
        # Ramp Lg
        Lg = ramp(0.86, 6.0, 2.5, t)

        # Forces into x and y components based on fpa
        FLx = Lg * math.sin(fpa)
        FLy = Lg * math.cos(fpa)

        FWx = 0.0
        FWy = -Wg

        FDx = -Dg * math.cos(fpa)
        FDy = Dg * math.sin(fpa)

        # Sum the forces in x and y
        Fx = FLx + FWx + FDx
        Fy = FLy + FWy + FDy

        # Integrate forces/acceleration to get delta velocity in x and y
        dVx = Fx * g * dt
        dVy = Fy * g * dt

        # Resultant velocities
        Vx = Vx + dVx
        Vy = Vy + dVy

        Vkt = magnitude(Vx, Vy) * msTokt

        # Integrate Vy to update altitude
        alt = alt + Vy * dt

        # Determine new fpa
        fpa = math.atan2(-Vy, Vx)

        # Increment time
        t = t + dt

        # Print some results
        print(math.degrees(fpa), alt*mToft, Vkt)

        times.append(t)
        alts.append(alt*mToft)

    ax.plot(times, alts, label='%d degrees' % (initialFPA + 0.5))
    ax.legend(loc='upper right') 
    ax.set_xlabel('Time (s)') 

# Runs
#gPullOut(480, 45)
#gPullOut(540, 45)
#gPullOut(600, 45)

startAlt = 10000
ias = 500
gPull = 6

ax.set_title("%dg Pull-out at %dkt" % (gPull, ias))

gPullOut(IAStoTAS(ias, startAlt), 30)
gPullOut(IAStoTAS(ias, startAlt), 45)
gPullOut(IAStoTAS(ias, startAlt), 60)
gPullOut(IAStoTAS(ias, startAlt), 89.9)

plt.show()

print("Finished")