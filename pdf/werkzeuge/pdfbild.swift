import PDFKit
import AppKit
let args = CommandLine.arguments
let doc = PDFDocument(url: URL(fileURLWithPath: args[1]))!
let ziel = args[2]
for i in 0..<doc.pageCount {
    let p = doc.page(at: i)!
    let r = p.bounds(for: .mediaBox)
    let s: CGFloat = 1.6
    let img = NSImage(size: NSSize(width: r.width*s, height: r.height*s))
    img.lockFocus()
    NSColor.white.setFill(); NSRect(x: 0, y: 0, width: r.width*s, height: r.height*s).fill()
    let ctx = NSGraphicsContext.current!.cgContext
    ctx.scaleBy(x: s, y: s)
    p.draw(with: .mediaBox, to: ctx)
    img.unlockFocus()
    let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
    try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: "\(ziel)/pdf-\(i+1).png"))
}
print(doc.pageCount)
