*AI Weekly · Episode 01*

# How Diffusion Models Learn to Dream in Pixels

**Runtime target:** ~10:00 **Narration:** ~1,200 words **Segments:** 9 **Topic:** AI Diffusion Models

**Stand:** Skript und Lizenzprüfung der Abbildungen sind fertig, Vertonung und Videoschnitt stehen noch aus.

## Lizenzprüfung der Abbildungen (vor dem Schreiben)

| Paper                                                                      | arXiv      | Result                                                 |
|----------------------------------------------------------------------------|------------|--------------------------------------------------------|
| Luo — *Understanding Diffusion Models: A Unified Perspective*              | 2208.11970 | CC BY 4.0 — cleared      |
| Kazerouni et al. — *Diffusion Models for Medical Image Analysis: A Survey* | 2211.07804 | CC BY 4.0 — cleared      |
| Ho, Jain, Abbeel — *DDPM*                                                  | 2006.11239 | non-exclusive — excluded |
| Rombach et al. — *Latent/Stable Diffusion*                                 | 2112.10752 | non-exclusive — excluded |
| Dhariwal & Nichol — *Diffusion Models Beat GANs*                           | 2105.05233 | non-exclusive — excluded |
| Karras et al. — *EDM*                                                      | 2206.00364 | non-exclusive — excluded |

## Storyboard und Sprechertext

### 1 · Title card

*0:00–0:10 · Silent*

Series wordmark + "Episode 01 — How Diffusion Models Learn to Dream in Pixels." No narration.

### 2 · Hook

*0:10–0:55 · Hook*

Every image Stable Diffusion or Midjourney generates starts as pure static — literally, random noise, the same kind you'd see on an old analog TV. And yet, twenty steps later, out comes a photorealistic astronaut riding a horse on Mars. How does a model turn nothing into something that specific? The answer is a strange and elegant idea borrowed from physics: teach a neural network to run entropy backwards. This is how diffusion models work — and once you see the mechanism, you'll never look at an AI-generated image the same way.

### 3 · Problem framing

*0:55–1:55 · Context*

Before diffusion models, the dominant approach to image generation was GANs — two networks fighting each other, one generating fakes, one trying to catch them. GANs could produce sharp images fast, but they were notoriously unstable to train and prone to "mode collapse," producing the same few outputs over and over. Researchers wanted something more stable and better understood mathematically. The idea came from an unlikely place: nonequilibrium thermodynamics. A 2015 paper proposed that if you could model how a system diffuses toward random noise, you could, in principle, learn to reverse that process step by step. It took until 2020, with the "Denoising Diffusion Probabilistic Models" paper, for this idea to actually outperform GANs on image quality — and that paper kicked off the entire modern wave.

### 4 · Mechanism, part 1 — Forward process

*1:55–4:15 · Core*

Here's the trick, in two halves. Half one is the forward process, and it's almost insultingly simple: take a real image, and add a small amount of Gaussian noise to it. Take that slightly-noisier image, and add a little more noise. Repeat this a few hundred or a thousand times, and by the end, the original image is completely gone — what's left is indistinguishable from pure static. This is called a Markov chain: each step only depends on the step right before it, which keeps the math tractable. What's elegant — laid out clearly in Calvin Luo's 2022 paper "Understanding Diffusion Models: A Unified Perspective" — is that this forward chain is mathematically the same object as a hierarchical variational autoencoder. Instead of one encoder compressing an image in a single leap, you have hundreds of tiny, deterministic steps, each just adding a measured dose of noise. That framing matters because everything we already know about training VAEs — maximizing an evidence lower bound — carries over directly. You're not inventing new math for diffusion models; you're running the same variational machinery over many more, much smaller steps. And smaller steps are the whole trick: because each individual step is such a tiny, local corruption, the reverse of that step is something a neural network can actually learn.

**Visual:** Luo Fig. — hierarchical Markov chain diagram (VAE ⇄ diffusion unification). On-screen citation required.

Luo, C. (2022) arXiv:2208.11970 · CC BY 4.0

### 5 · Mechanism, part 2 — Reverse process

*4:15–6:35 · Core*

So half two is the reverse process, and this is where the actual neural network lives. You train a model — usually a U-Net, the same architecture used for image segmentation — to look at a noisy image and predict the noise that was added to it. Not the clean image directly, just the noise. Once you can predict the noise at any step, you can subtract a bit of it out, nudging the image toward "less noisy," and repeat. Do that a thousand times in reverse, starting from pure random static, and you arrive at a plausible, sharp image the network has essentially hallucinated one denoising step at a time. What makes this powerful is that the same math generalizes far beyond photos of cats and landscapes. The 2022 survey "Diffusion Models for Medical Image Analysis," by Kazerouni and colleagues, catalogs this same forward-noise, reverse-denoise mechanism applied to MRI reconstruction, tumor segmentation, and anomaly detection — because the network isn't learning "what a photo looks like," it's learning "how to undo a specific, well-understood kind of corruption," a skill that transfers to any signal you can meaningfully add noise to.

**Visual:** Kazerouni et al. taxonomy figure — family tree of diffusion variants across applications. On-screen citation required.

Kazerouni et al. (2022) arXiv:2211.07804 · CC BY 4.0

### 6 · Results & evidence

*6:35–8:05 · Evidence*

Does this actually work better than the alternatives? By 2021, diffusion models were beating state-of-the-art GANs on standard image-quality benchmarks like FID score on ImageNet, while also being far more stable to train, since there's no adversarial min-max game that can collapse. The tradeoff is speed: a GAN generates an image in one forward pass; a classic diffusion model needs hundreds or thousands of denoising steps, which is slow. That single weakness spawned its own research arms race — techniques like DDIM sampling and later distillation methods cut generation down from a thousand steps to as few as twenty or even four, which is what makes tools like Stable Diffusion usable in a few seconds on a consumer GPU today.

**Visual:** original redrawn chart — steps-vs-quality tradeoff curve (no copyrighted source; built fresh in series style, since the originating benchmark figures aren't cleared for reuse).

### 7 · Limitations & open questions

*8:05–9:05 · Caveat*

Diffusion models aren't magic, though. They're compute-hungry to train, and they can still hallucinate anatomically wrong details — extra fingers, garbled text — because they're pattern-completing noise, not reasoning about anatomy. And because they're trained on internet-scraped images, they inherit every bias and copyright question baked into that data — which, ironically, is exactly the kind of licensing question we had to navigate just to make this episode, since most of the landmark diffusion papers keep their own figures copyrighted by default. Researchers are still working on making sampling faster, more controllable, and more faithful to prompts without needing the retraining newer techniques increasingly avoid.

### 8 · Recap & next-week teaser

*9:05–9:45 · Close*

So: diffusion models learn by destroying images with noise, step by tiny step, and then training a network to undo exactly that. It's the same idea underneath Stable Diffusion, DALL·E's newer versions, and a growing share of medical and scientific imaging tools. Next week, we'll stay in the generative AI family and look at the mechanism that made large language models actually usable at scale: attention, and why "Attention Is All You Need" turned out to be true. See you then.

### 9 · End card

*9:45–10:00 · Silent*

Full source list + licenses on screen. Series wordmark. No narration.

≈1,200 narrated words · ~8:00 spoken at 150 wpm + title/end-card holds ≈ 10:00 total

## Full source list (end-card text)

1.  Luo, C. (2022). *Understanding Diffusion Models: A Unified Perspective.* `arXiv:2208.11970`. License: CC BY 4.0.
2.  Kazerouni, A., Aghdam, E. K., Heidari, M., Azad, R., Fayyaz, M., Hacihaliloglu, I., Merhof, D. (2022). *Diffusion Models for Medical Image Analysis: A Comprehensive Survey.* `arXiv:2211.07804`. License: CC BY 4.0.
3.  Steps-vs-quality tradeoff chart and process diagrams for DDPM/Stable Diffusion concepts: original illustrations created for this series, not reproduced from copyrighted source figures.

