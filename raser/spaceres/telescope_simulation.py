#!/usr/bin/env python3

from pathlib import Path

import acts
import acts.examples
from acts.examples.simulation import (
    addParticleGun,
    EtaConfig,
    PhiConfig,
    ParticleConfig,
    addFatras,
)

u = acts.UnitConstants

if "__main__" == __name__:
    detector, trackingGeometry, decorators = acts.examples.TelescopeDetector.create(
        positions=[20, 60, 100, 140, 180, 220],
        bounds=[200, 200],
        binValue=2,
    )

    field = acts.ConstantBField(acts.Vector3(0, 0, 0 * u.T))

    outputDir = Path.cwd() / "output/telescope_simulation"
    if not outputDir.exists():
        outputDir.mkdir()

    rnd = acts.examples.RandomNumbers(seed=42)

    s = acts.examples.Sequencer(events=1, numThreads=1, logLevel=acts.logging.INFO)
    
    postfix = "fatras"
    
    addParticleGun(
        s,
        EtaConfig(-10.0, 10.0),
        PhiConfig(0.0, 360.0 * u.degree),
        ParticleConfig(1000, acts.PdgParticle.eMuon, False),
        multiplicity=1,
        rnd=rnd,
        outputDirRoot=outputDir / postfix,
    )
   
    addFatras(
        s,
        trackingGeometry,
        field,
        rnd=rnd,
        outputDirRoot=outputDir / postfix,
    )
    
    

    s.run()