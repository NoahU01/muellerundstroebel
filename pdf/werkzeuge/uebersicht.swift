import AppKit
let a = CommandLine.arguments
let files = Array(a[2...])
let w: CGFloat = 476, h: CGFloat = 674, cols = 4
let rows = (files.count + cols - 1) / cols
let out = NSImage(size: NSSize(width: w*CGFloat(cols)+CGFloat(cols+1)*12, height: h*CGFloat(rows)+CGFloat(rows+1)*12))
out.lockFocus(); NSColor.gray.setFill(); NSRect(origin: .zero, size: out.size).fill()
for (i,f) in files.enumerated() { let img = NSImage(contentsOfFile: f)!; let c = i % cols, r = i / cols
  img.draw(in: NSRect(x: 12+CGFloat(c)*(w+12), y: out.size.height-CGFloat(r+1)*(h+12), width: w, height: h)) }
out.unlockFocus()
try! NSBitmapImageRep(data: out.tiffRepresentation!)!.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[1]))
